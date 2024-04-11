import time
import logging
from dataclasses import dataclass
from datetime import datetime, date, timedelta

from bs4 import BeautifulSoup, Tag

from browsers.pages import Page
from proposal_sender.base_job import Job
from proposal_sender.platforms.base import Platform
from proposal_sender.platforms.utils import pad_message, requires_page
from proposal_sender.settings import CAN_HELP_MESSAGE_TEMPLATE
from proposal_sender.data import save_jobs

# Pages
job_list_page = Page('https://www.wyzant.com/tutor/jobs')
login_page = Page('https://www.wyzant.com/login')

# Messages
CAN_HELP_MESSAGE_TEMPLATE = CAN_HELP_MESSAGE_TEMPLATE
UNABLE_TO_HELP_MESSAGE_TEMPLATE = 'Dear {client_name}, While there are probably some things I can help you with, unfortunately I\'m not currently at a level where I can help you with this project 100%. I\'m sending you this because Wyzant doesn\'t have an option to remove a job from my view of jobs available. If you\'ve read my profile and think I could help you, feel free to reach out :) I appreciate your understanding and wish you the best. Respectfully, Zack P.'
OLD_JOB_MESSAGE_TEMPLATE = 'Hey {client_name}! I\'d love to help you with this 🙂 but it looks like you posted this a while ago. If you happen to still want any {subject} help, I\'d love to assist you 🙂. Please feel free to reach out.'


class Wyzant(Platform):
    base_url = 'https://www.wyzant.com'
    min_message_chars = 150
    min_time_before_refresh = 60  # Seconds
    refresh_load_time = 0  # Seconds
    login_wait_time = 3  # Seconds


    def autopilot(self):
        """Automatically apply to (or ignore) jobs on codementor continuously."""
        logging.info('🐜 Starting Wyzant Autopilot 🐜')
        while True:
            start_time = time.time()
            self.send_proposals()
            end_time = time.time()
            total_time = end_time - start_time
            if total_time < self.min_time_before_refresh:
                time.sleep(self.min_time_before_refresh - total_time)
            self.refresh_jobs()
            time.sleep(self.refresh_load_time)  # Wait after refresh
    
    def send_proposals(self):
        """Send proposals to all jobs"""
        jobs = self.get_jobs()
        for job in jobs:
            job.evaluate(manual=self.evaluate_manually)
        for job in jobs:
            self.apply(job)
        if jobs:
            save_jobs(jobs)

    def login(self):
        logging.info('🔐 Logging in to Wyzant 🔐')
        self.browser.open_page(login_page)
        username, password = self.get_login_info()
        username_field = self.browser.find_elements('id', 'Username')[-1]
        password_field = self.browser.find_elements('id', 'Password')[-1]
        buttons = self.browser.find_elements('css selector', 'button[type="submit"]')
        submit_button = [button for button in buttons if button.text == 'LOG IN'][0]
        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()
        time.sleep(self.login_wait_time)

    @requires_page(job_list_page)
    def get_jobs(self) -> list['WyzantJob']:
        job_cards = self._get_all_job_cards()
        jobs = [WyzantJob.from_card(card) for card in job_cards]
        if jobs:
            logging.info(f'🥳 {len(jobs)} new jobs found! 🥳')
        return jobs

    def _get_all_job_cards(self):
        job_count = self._get_job_count()
        page_count = self._get_page_count()
        all_job_cards = []
        if job_count:
            for page_number in range(1, page_count + 1): 
                self.browser.open_page(job_list_page.with_params(page=page_number))
                soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                job_cards = soup.find_all('div', class_='academy-card')
                all_job_cards.extend(job_cards)
        return all_job_cards
    
    def _get_page_count(self) -> int:
        """Get number of pages of jobs"""
        available_jobs = self._get_job_count()
        page_count = available_jobs // 10 + 1
        return page_count

    @requires_page(job_list_page)
    def _get_job_count(self) -> int:
        """Get number of pages of jobs"""
        job_list_page_html = self.browser.page_source
        soup = BeautifulSoup(job_list_page_html, 'html.parser')
        job_count = int(soup.select_one('h2 > span').text)
        return job_count


    def apply(self, job: 'WyzantJob'):
        """Send a message to all jobs that haven't had a message sent yet."""
        logging.info(f'🚀 Applying to job: {job.url} 🚀')
        self.open_job(job)
        message = self.build_message(job)
        message_texarea = self.browser.find_element('id', 'personal_message')
        self.browser.send_keys_with_emojis(message_texarea, message)
        job.initial_message = message

        # Click 'Agree to hourly rate' checkbox if it exists
        try:
            agree_to_hourly_rate_checkbox = self.browser.find_element('css selector', '#agree_partner_hourly_rate')
            agree_to_hourly_rate_checkbox.click()
        except:
            pass

        submit_button = self.browser.find_element('css selector', '#job_application_form > input.btn.old-button-color')
        submit_button.click()
        job.applied = True

    def build_message(self, job: 'WyzantJob') -> str:
        """Build a message to send to the client based on the job's evaluation"""
        message = ''
        if job.evaluation == 'Can Help':
            message = CAN_HELP_MESSAGE_TEMPLATE.format(**vars(job))
        elif job.evaluation == 'Unable to Help':
            message = UNABLE_TO_HELP_MESSAGE_TEMPLATE.format(**vars(job))
        elif job.evaluation == 'Old Job':
            message = OLD_JOB_MESSAGE_TEMPLATE.format(**vars(job))
        return pad_message(message, self.min_message_chars)
    
    @requires_page(job_list_page)
    def refresh_jobs(self):
        """Refresh job list"""
        self.browser.refresh()
        logging.info('🔄 Refreshed jobs! 🔄')

JOB_INFO_TEMPLATE = """\
Client: {client_name}
Subject: {subject}
Description: {description}
Date Published: {publish_date}\
"""

@dataclass
class WyzantJob(Job):
    platform: str = Wyzant.name
    subject: str | None = None

    def __str__(self):
        return JOB_INFO_TEMPLATE.format(**vars(self))

    @classmethod
    def from_card(cls, job_card: Tag):
        """Create a job from a Wyzant job card."""
        data = cls._parse_data_from_job_card(job_card)
        return cls(**data)

    def evaluate(self, manual=False):
        """Decide which jobs you can help with"""
        if self.contains_blocked_expertise():
            self.evaluation = 'Unable to Help'
            self.evaluation_method = 'automatic'
        elif self.is_old():
            self.evaluation = 'Old Job'
            self.evaluation_method = 'automatic'
        elif not manual:
            self.evaluation = 'Can Help'
            self.evaluation_method = 'automatic'
        else:
            can_help = input(f'{self}\n\nCan you help with this job? (y/n): ') == 'y'
            print()
            self.evaluation_method = 'manual'
            if can_help:
                self.evaluation = 'Can Help'
            else:
                self.evaluation = 'Unable to Help'
        if self.evaluation == 'Can Help':
            logging.info(f'✅ Approved {self.subject} job: {self.url} ✅')
        elif self.evaluation == 'Unable to Help':
            logging.info(f'🚫 Rejected {self.subject} job: {self.url} 🚫')
        elif self.evaluation == 'Old self':
            logging.info(f'👴 Old {self.subject} job: {self.url} 👵')

    def is_old(self):
        if self.publish_date:
            return self.publish_date < datetime.now() - timedelta(days=7)

    @staticmethod
    def _parse_data_from_job_card(job_card: Tag) -> dict:
        """Parse job from job card"""
        soup = BeautifulSoup(str(job_card), 'html.parser')
        url = Wyzant.base_url + soup.find('a', class_='job-details-link')['href']  # type: ignore
        subject = soup.find('a', class_='job-details-link').text
        description = soup.find('p', class_='job-description').text
        client_name = soup.select_one('p.text-semibold.spc-zero-n.spc-tiny-s').text.strip()
        publish_date = WyzantJob._parse_publish_date(soup.select_one('div.pull-right.small-hide > span.text-semibold.text-light').text)
        return {
            'url': url,
            'subject': subject,
            'description': description,
            'client_name': client_name,
            'publish_date': publish_date,
        }

    @staticmethod
    def _parse_publish_date(date_string: str) -> date:
        """Parse Wyzant time string into datetime object"""
        date_string = date_string.strip()
        if date_string.endswith('m'):  # 10m, 20m, 30m, etc.
            return datetime.now() - timedelta(minutes=int(date_string[:-1]))
        if date_string.endswith('h'):  # 2h, 3h, 4h, etc.
            return datetime.now() - timedelta(hours=int(date_string[:-1]))
        elif date_string.endswith('d'):  # 2d, 3d, 4d, etc.
            return datetime.now() - timedelta(days=int(date_string[:-1]))
        else:  # Jan 1, Feb 2, Mar 3, etc.
            dt = datetime.strptime(date_string, '%b %d')
            dt = dt.replace(year=datetime.now().year)
            return dt
