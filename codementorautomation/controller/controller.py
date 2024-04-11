import logging
import time
from dataclasses import dataclass 

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import Session as DBSession
from database.models import Job, User
from utils import build_options
from webscraper import CodementorWebScraper 
from .message_templates import MESSAGE_TEMPLATE


@dataclass
class CodementorController:
    driver: WebDriver
    session: Session = None

    def __post_init__(self):
        load_dotenv()
        if not self.session:
            self.session = DBSession()
        self.webscraper = CodementorWebScraper.start(self.driver)

    @classmethod
    def start(cls, options=build_options()):
        driver = webdriver.Chrome(options=options)
        return cls(driver)

    def watch_jobs(self, seconds_between_refresh: int = 10):
        """Watch, update, evaluate, and apply to new jobs."""
        logging.info('🦅 Watching jobs...')
        while True:
            start = time.time()
            self.get_and_apply_to_new_jobs()
            remaining_time = seconds_between_refresh - (time.time() - start)
            if remaining_time > 0:
                time.sleep(remaining_time)
            self.webscraper.refresh_jobs()

    def apply_to_applicable_jobs(self) -> list[Job]:
        """Apply to all applicable jobs."""
        applicable_jobs = Job.get_applicable(self.session)
        logging.info(f'🥳 {len(applicable_jobs)} applicable jobs found.')
        if applicable_jobs:
            for i, job in enumerate(applicable_jobs, 1):
                self.apply_to_job(job, message=MESSAGE_TEMPLATE.format(user=job.user))
        return applicable_jobs

    def get_and_apply_to_new_jobs(self) -> list[Job]:
        """Get new jobs and apply to them if possible."""
        new_jobs = self.get_new_jobs()
        if new_jobs:
            for job in new_jobs:
                self.update_job(job)
                if job.is_applicable():
                    logging.info(f'✅ Job is applicable.')
                    self.apply_to_job(job, message=MESSAGE_TEMPLATE.format(user=job.user))
                else:
                    logging.info(f'❌ Job is not applicable!')
        return new_jobs

    def update_and_apply_to_job(self, job: Job, logs: bool = True) -> Job:
        """Update all jobs and apply to them if possible."""
        self.update_job(job, logs=logs)
        if job.is_applicable():
            self.apply_to_job(job, message=MESSAGE_TEMPLATE.format(user=job.user), logs=logs)
            return job
    
    def update_and_apply_to_jobs(self, jobs: list[Job], seconds_between_updates: int = 0) -> list[Job]:
            logging.info(f'👀 Updating and applying to {len(jobs)} jobs.')
            for i, job in enumerate(jobs, 1):
                logging.debug(f'🔃 Updating and applying to job ({i} of {len(jobs)}) : {job.url}')
                self.update_and_apply_to_job(job)
                if seconds_between_updates:
                    time.sleep(seconds_between_updates)
            return jobs

    def apply_to_job(self, job: Job, message: str, logs: bool = True) -> None:
        """Apply to a job, saving the application and updated job to the database.

        :param job: The job to apply to.
        :type job: Job
        :param message: The message to send to the user. The given message template has access to the job object.
        :type message: str
        :param logs: Whether to log the application, defaults to True
        :type logs: bool, optional

        """
        if not job.is_applicable():
            feedback = f'🚫 Job was passed that was not applicable: {job}'
            feedforward = '➡️ Make sure the job is applicable before applying to it.'
            raise ValueError(f'{feedback}\n{feedforward}')
        if logs:
            logging.debug(f'📝 Applying to job: {job.url}')
        application = self.webscraper.apply_to_job(job, message.format(job=job, user=job.user))
        self.session.add(application)
        job.is_applied_to = True
        self.session.commit()
        if logs:
            logging.info(f'✅ Successfully applied to job: {job.url}')

    def get_new_jobs(self) -> list[Job]:
        """Get all new job postings from codementor's Open Requests page."""
        existing_jobs = Job.all(self.session)
        new_jobs = self.webscraper.get_new_jobs(existing_jobs)
        if new_jobs:
            logging.info(f'🎉 {len(new_jobs)} new jobs found!')
            self.session.add_all(new_jobs)
            self.session.commit()
            logging.info(f'💽 {len(new_jobs)} jobs saved!')
        else:
            logging.debug('🪹 No new jobs found.')
        return new_jobs

    def update_job(self, job: Job, logs: bool = True):
        """Update a job with its latest details."""
        try:
            logging.debug(f'🔃 Attempting to update job: {job.url}')
            _, user = self.webscraper.update_job(job)
            if not user.exists(self.session):
                user.add(self.session)
            else:
                user = User.get(self.session, url=user.url).update(user)
            job.user = user
            job.evaluate(self.session)
            self.session.commit()
            logging.info(f'⬆️ Job updated: {job.url}')
            return job
        except WebDriverException as e:
            if 'cannot deserialize the result value received from Runtime.callFunction' in str(e):
                logging.exception(str(e))
                logging.info('🚫 Ignoring job due to emoji in name.')
                job.is_ignored = True
                self.session.commit()


    def update_jobs(self, jobs: list[Job], seconds_between_updates: int = 0) -> list[Job]:
        """Update jobs in a list of jobs with their latest details."""
        job_count = len(jobs)
        logging.info(f'👀 Updating {job_count} jobs.')
        for i, job in enumerate(jobs, 1):
            logging.debug(f'🔃 Attempting to update job ({i} of {job_count}): {job.url}')
            self.update_job(job, logs=False)
            logging.info(f'⬆️ Job updated ({i} of {job_count}): {job.url}')
            if seconds_between_updates:
                time.sleep(seconds_between_updates)
        logging.info(f'🥳 {len(jobs)} jobs updated!')
        return jobs

    def update_incomplete_jobs(self, seconds_between_updates: int = 0) -> list[Job]:
        """Update all jobs that are not fully updated."""
        jobs = Job.filter_by(self.session, is_fully_updated=False).all()
        logging.info(f'👀 {len(jobs)} incomplete jobs to update.')
        self.update_jobs(jobs, seconds_between_updates)
        logging.info('🥳 Incomplete jobs updated!')
        return jobs

    def update_all_jobs(self, seconds_between_updates: int = 0) -> list[Job]:
        """Update all jobs."""
        jobs = Job.all(self.session)
        logging.info(f'👀 {len(jobs)} jobs to update.')
        self.update_jobs(jobs, seconds_between_updates)
        logging.info('🥳 All jobs updated!')
        return jobs