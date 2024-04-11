import time
import logging

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.chrome.service import Service
from wyzantapi import WyzantAPI

import logger
from models import Job, AutomationError
from message_templates import GENERAL_MESSAGE
from settings import DATA_DIR, SCREENSHOTS_DIR, MIN_RATE

logger = logging.getLogger('wyzantautomation')


class Automation:

    def __init__(self, headless: bool = True, refresh_time: float = 60, rate: int = MIN_RATE):
        self.refresh_time = refresh_time
        self.rate = rate
        logger.info(f'💲 Starting with minimum rate: {rate}')
        options = self._build_driver_options(headless=headless, logging=False)
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        self.api = WyzantAPI.start(driver)
        logger.info('⚙️ Automation started')

    @classmethod
    def start(cls, **kwargs):
        """Start the automation."""
        automation = cls(**kwargs)
        automation.run()

    def run(self):
        """Run the automation with error handling."""
        try:
            self.mainloop()
        except KeyboardInterrupt:
            logger.info('⚠️ Automation stopped due to keyboard interrupt.')
        except (NoSuchWindowException, ConnectionResetError):
            logger.info('⚠️ Automation stopped due to window being closed.')
        except Exception as e:
            logger.info('⚠️ Automation stopped due to error.')
            time_str = time.strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_path = str(SCREENSHOTS_DIR / f'error {time_str}.png')
            self.api.driver.save_screenshot(screenshot_path)
            automation_error = AutomationError(
                url=self.api.driver.current_url,
                screenshot_path=screenshot_path,
                message=str(e),
            )
            logger.exception(str(automation_error))
            logger.exception(e)
            self.api.driver.quit()
            raise e

    def mainloop(self):
        """The main loop of the automation.
        Args:
            headless (bool, optional): Whether to run the automation in headless mode. Defaults to True.
            refresh_time (int, optional): How often to refresh the page in seconds. Defaults to 60.
        """
        logger.info('🔍 Searching for jobs...')
        while True:
            start_time = time.time()
            jobs = self.api.get_jobs()
            if jobs:
                logger.info(f'🎉 Found {len(jobs)} job{"s" if len(jobs) > 1 else ""}!')
                self.apply_to_jobs(jobs)
                self.save_jobs(jobs)
            else:
                logger.debug('🪹 No jobs found.')
            end_time = time.time()
            total_time = end_time - start_time
            time_remaining = self.refresh_time - total_time
            if time_remaining > 0:
                logger.debug(f'⌚ Job search done in {total_time:.2f} seconds...')
                logger.debug(f'😴 Sleeping {time_remaining:.2f} seconds...')
                time.sleep(time_remaining)
            logger.debug(f'🔄 Refreshing page...')
            self.api.driver.refresh()
            
            
    def apply_to_jobs(self, jobs: list[Job]):
        """Apply to a list of jobs."""
        for job in jobs:
            self.apply_to_job(job)

    def apply_to_job(self, job: Job):
        """Apply to a job."""
        logger.debug(f'🚀 Applying to job: {job.url}')
        try:
            # Set rate to None if it doesn't exist
            rate = self.rate
            if rate and job.recommended_rate:
                rate = self.rate if not job.recommended_rate > self.rate else job.recommended_rate
            self.api.apply_to_job(job, GENERAL_MESSAGE.format(job=job), rate=rate)
            logger.info(f'✅ Applied to job at rate ${job.application.rate}: {job.url}')
        except Exception as e:
            logger.exception(e)
            logger.error(f'🚫 Failed to apply to job: {job.url}')

    def save_jobs(self, jobs: list[Job]):
        """Save jobs to csv."""
        # Create jobs data
        df = pd.DataFrame([job.model_dump() for job in jobs])

        # Write jobs to csv
        jobs_csv = DATA_DIR / 'jobs.csv'
        if jobs_csv.exists():
            df.to_csv(jobs_csv, index=False, mode="a", header=False)
        else:
            df.to_csv(jobs_csv, index=False)

    def _build_driver_options(self, headless=True, logging=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        # Remove selenium logging
        if not logging:
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return options


if __name__ == '__main__':
    Automation.start()