import os

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from selenium.webdriver.remote.webdriver import WebDriver

from .models import Account, Job
from .pages import LoginPage, JobListPage, JobDetailPage
from .constants import JOBS_PER_PAGE


class WyzantAPI(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    account: Account
    driver: WebDriver | None = None

    @classmethod
    def start(cls, driver: WebDriver) -> 'WyzantAPI':
        wyzant = cls.from_env(driver)
        success = wyzant.login()
        if not success:
            raise Exception('Login unsuccessful')
        return wyzant

    @classmethod
    def from_env(cls, driver: WebDriver) -> 'WyzantAPI':
        load_dotenv()
        return cls(
            account=Account(
                username=os.getenv('WYZANT_USERNAME'),
                password=os.getenv('WYZANT_PASSWORD')
            ),
            driver=driver
        )

    def login(self) -> bool:
        success = LoginPage.bring(self.driver).login(self.account)
        return success

    def get_jobs(self) -> list[Job]:
        jobs: list[Job] = []
        job_count = self.get_job_count()
        if job_count > 0:
            page_count = (job_count // JOBS_PER_PAGE) + 1
            for page_num in range(1, page_count + 1):
                page_jobs = JobListPage.bring(self.driver, page=page_num).get_jobs()
                jobs.extend(page_jobs)
        return jobs

    def apply_to_job(self, job: Job, message: str, rate: int | None = None) -> None:
        job_detail_page = JobDetailPage.bring(self.driver, instance=job)
        # NOTE: Adding the payment_info_on_file is a side effect because 
        # currently the jobs are only pulled from the list page, and the 
        # payment_info_on_file field is only available on the detail page.
        job.student.payment_info_on_file = job_detail_page.get_payment_info_on_file()  
        job.application = job_detail_page.apply(message, rate)
        job.application.job_id = job.id

    def get_job_count(self) -> int:
        return JobListPage.bring(self.driver).get_job_count()
