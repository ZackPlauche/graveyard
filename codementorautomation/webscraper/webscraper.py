import logging
import os
from typing import Self

from pydantic import BaseModel, ConfigDict
from selenium.webdriver.remote.webdriver import WebDriver

from database.models import Job, Session, FreelanceJob, Application, User
from .types import LoginDetails
from .pages import LoginPage, JobListPage, SessionHistoryPage, FreelanceJobsPage, Dashboard, JobDetailPage


class CodementorWebScraper(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    login_details: LoginDetails
    driver: WebDriver

    @classmethod
    def start(cls, driver: WebDriver):
        logging.info('👨‍💻 Starting Codementor WebScraper...')
        codementor = cls.from_env(driver=driver)

        # If not already logged in, login
        Dashboard.bring(driver)
        if not codementor.driver.current_url == Dashboard.url:
            codementor.login()

        return codementor

    @classmethod
    def from_env(cls, driver: WebDriver) -> Self:
        email = os.getenv('CODEMENTOR_EMAIL')
        password = os.getenv('CODEMENTOR_PASSWORD')
        if all([email, password]):
            login_details = LoginDetails(email=email, password=password)
        else:
            raise Exception('Login details not found in environment variables.')
        return cls(login_details=login_details, driver=driver)

    def login(self):
        """Login to Codementor."""  # TODO: Add handler for reCaptcha popup
        LoginPage.bring(self.driver).login(login_details=self.login_details)

    def get_new_jobs(self, existing_jobs: list[Job]) -> list[Job]:
        """Get all new job postings from codementor's Open Requests page."""
        new_jobs = []
        existing_job_urls = [job.url for job in existing_jobs]
        while True:
            jobs = self.get_loaded_jobs()
            existing_jobs_included = any([job.url in existing_job_urls for job in jobs])
            if existing_jobs_included:
                break
            self.load_more_jobs()
        new_jobs = [job for job in jobs if job.url not in existing_job_urls]
        return new_jobs

    def get_all_jobs(self) -> list[Job]:
        """Get all job postings from codementor's Open Requests page."""
        return JobListPage.bring(self.driver).scrape_jobs()

    def get_loaded_jobs(self) -> list[Job]:
        """Get all job postings that are currently loaded on the Open Requests page."""
        return JobListPage.bring(self.driver).scrape_loaded_jobs()
    
    def load_more_jobs(self) -> list[Job]:
        """Get more jobs on the Open Requests page."""
        JobListPage.bring(self.driver).load_more_job_cards()

    def update_job(self, job: Job) -> tuple[Job, User]:
        """Update the details of a job."""
        job_detail_page = JobDetailPage.bring(self.driver, instance=job)
        scraped_job = job_detail_page.scrape_job()
        scraped_user = job_detail_page.scrape_user()
        job.update(scraped_job)
        job.is_fully_updated = True
        return job, scraped_user

    def apply_to_job(self, job: Job, message: str) -> Application:
        """Apply to a request."""
        return JobDetailPage.bring(self.driver, instance=job).apply(message=message)

    def refresh_jobs(self):
        """Refresh all jobs without reloading the page."""
        JobListPage.bring(self.driver).click_job_list_refresh_button()
        

    # ------------------------------------------------------------------------------ Don't focus on right now #
    def get_session_list_data(self) -> list[Session]:
        """Get all sessions on the Session list page."""
        session_history_page = SessionHistoryPage.bring(driver=self.driver)
        sessions = session_history_page.get_sessions()
        return sessions

    def get_freelance_jobs(self) -> list[FreelanceJob]:
        freelance_jobs_page = FreelanceJobsPage.bring(driver=self.driver)
        freelance_jobs = freelance_jobs_page.get_freelance_jobs()
        return freelance_jobs
