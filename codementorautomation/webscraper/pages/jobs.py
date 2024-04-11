import logging
from datetime import datetime

from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

from webscraper.elements.jobs import JobDetails, JobCardList, JobCard, JobInterestForm, RefreshJobsButton
from webscraper.elements.chatbox import Chatbox
from webscraper.elements.popups import InstantHelpRequestPopup, SessionNoticePopup
from database.models import Job, Application, User
from .base import BasePage, BaseDetailPage


class JobListPage(BasePage):
    url = 'https://www.codementor.io/m/dashboard/open-requests'

    def scrape_jobs(self) -> list[Job]:
        """Scrape all jobs on the page."""
        return [card.scrape_job() for card in self.get_job_cards()]

    def scrape_loaded_jobs(self) -> list[Job]:
        """Scrape jobs that are currently loaded on the page."""
        return [card.scrape_job() for card in self.get_loaded_job_cards()]

    def scrape_more_jobs(self) -> list[Job]:
        """Scrape more jobs on the page."""
        return [card.scrape_job() for card in self.get_more_job_cards()]

    def get_job_cards(self) -> list[JobCard]:
        """Get all job cards on the page."""
        return JobCardList.find(self.driver).get_items()

    def get_loaded_job_cards(self) -> list[JobCard]:
        """Get job cards that are currently loaded on the page."""
        return JobCardList.find(self.driver).get_loaded_items()

    def get_more_job_cards(self) -> list[JobCard]:
        """Get more job cards on the page."""
        return JobCardList.find(self.driver).get_more_items()

    def load_more_job_cards(self) -> None:
        """Load more job cards on the page."""
        JobCardList.find(self.driver).load_more_items()
    
    def load_job_cards(self) -> None:
        """Load all job cards on the page."""
        JobCardList.find(self.driver).get_items()

    def click_job_list_refresh_button(self) -> None:
        """Refresh jobs to see if new ones arrived without reloading the page."""
        try:
            RefreshJobsButton.find(self.driver).click()
            logging.debug('🔄 Clicked Refresh Jobs Button')
            return
        except ElementClickInterceptedException as e:
            try:
                InstantHelpRequestPopup.find(self.driver).remove()
                return
            except NoSuchElementException:
                pass
            try:
                SessionNoticePopup.find(self.driver).remove()
                return
            except NoSuchElementException:
                pass
            raise e
            


class JobDetailPage(BaseDetailPage):
    model = Job

    def scrape_job(self) -> Job:
        """Scrape job details. Assumes that the client has already been applied to if
        interst message has been sent.
        """
        job = JobDetails.find(self.driver).scrape_job()
        job.is_applied_to = JobInterestForm.find(self.driver).interest_message_sent
        return job

    def scrape_user(self) -> User:
        """Scrape the user that posted the job."""
        return JobDetails.find(self.driver).scrape_user()

    def apply(self, message: str) -> Application:
        """Apply to a job and return Application data."""
        try:
            job_interest_form = JobInterestForm.find(self.driver)
            job_interest_form.send_interest_message(message)
        except:
            pass
        job_interest_form = JobInterestForm.find(self.driver)  # Page reloads after sending interest message, so need to send again.
        job_interest_form.click_message_client_button()
        Chatbox.find_by_user(self.driver, self.instance.user).send_message(message)
        return Application(
            job=self.instance, 
            message=message,
            sent_at=datetime.utcnow(), 
            user=self.instance.user
        )