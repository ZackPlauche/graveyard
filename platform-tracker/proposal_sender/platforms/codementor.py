import time
import logging
from dataclasses import dataclass
from datetime import datetime
from functools import wraps

from bs4 import BeautifulSoup, Tag
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.remote.webelement import WebElement

from browsers import Page, Browser
from proposal_sender.base_job import Job
from proposal_sender.data import save_jobs
from proposal_sender.platforms.base import Platform
from proposal_sender.platforms.utils import requires_page, build_screenshot_path, screenshot_on_error
from proposal_sender.settings import CAN_HELP_MESSAGE_TEMPLATE

# Pages
job_detail_page = Page(url='', load_time=4)
job_list_page = Page('https://www.codementor.io/m/dashboard/open-requests', load_time=3)
related_job_list_page = job_list_page.with_params(expertise='related')
login_page = Page('https://arc.dev/login?service=codementor')


class Codementor(Platform):
    base_url = 'https://www.codementor.io'
    first_run = True
    detail_page = job_detail_page
    login_page = login_page
    min_time_before_refresh = 30  # Seconds
    job_refresh_load_time = 2  # Seconds
    job_scroll_load_time = 2  # Seconds
    login_wait_time = 5  # Seconds

    def autopilot(self):
        """Automatically apply to (or ignore) jobs on codementor continuously."""
        logging.info('🚀 Starting Codementor Autopilot 🚀')
        while True:
            start_time = time.time()
            self.send_proposals()
            end_time = time.time()
            total_time = end_time - start_time
            if total_time < self.min_time_before_refresh:
                time.sleep(self.min_time_before_refresh - total_time)
            self.refresh_jobs()
            time.sleep(self.job_refresh_load_time)  # Wait after refresh

    def send_proposals(self):
        """Send proposals to jobs on codementor."""
        # Load all job cards on the first run
        if self.first_run:
            self.load_all_job_cards()
        jobs = self.get_jobs()
        jobs = [job for job in jobs if not job.read]
        self.update_jobs(jobs)
        jobs = [job for job in jobs if not job.applied]
        for job in jobs:
            job.evaluate(manual=self.evaluate_manually)
        can_help_jobs = [job for job in jobs if job.can_help]
        for job in can_help_jobs:
            self.apply(job)
        if jobs:
            save_jobs(jobs)
        self.first_run = False

    @screenshot_on_error()
    def login(self):
        """Login to codementor."""
        logging.info('🔐 Logging in to Codementor 🔐')
        if not self.login_page.url in self.browser.url:
            self.browser.open_page(self.login_page)
        self.browser.open_page(login_page)
        username, password = self.get_login_info()
        self.browser.implicitly_wait(10)
        username_field = self.browser.find_element('css selector', 'input[name="email"]')
        password_field = self.browser.find_element('css selector', 'input[name="password"]')
        submit_button = self.browser.find_element('css selector', 'button[type="submit"]')
        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()
        time.sleep(self.login_wait_time)

    @requires_page(related_job_list_page)
    def get_jobs(self) -> list['CodementorJob']:
        """Get current jobs from the codementor open requests page."""
        job_cards = self.get_job_cards()
        jobs = [CodementorJob.from_job_card(job_card) for job_card in job_cards]
        return jobs

    def update_jobs(self, jobs: list['CodementorJob']):
        for job in jobs:
            self.update_job(job)

    @requires_page(related_job_list_page)
    def load_all_job_cards(self):
        """Show all job cards on the codementor open requests page."""
        logging.info('⛏️ Loading all jobs... ⛏️')
        previous_job_cards = []
        while True:
            visible_job_cards = self.get_job_cards()
            if len(visible_job_cards) > len(previous_job_cards):
                previous_job_cards = visible_job_cards
                self.browser.scroll_to_bottom()
                time.sleep(self.job_scroll_load_time)
                continue
            break

    @requires_page(related_job_list_page)
    def get_job_cards(self) -> list[Tag]:
        """Get visible job cards from codementor's job list page."""
        soup = BeautifulSoup(str(self.browser.page_source), 'html.parser')
        job_cards = soup.find_all('a', class_='dashboard__open-question-item')
        return job_cards

    def get_jobs_from_job_cards(self):
        """Get job objects from the job cards on the codementor job list page."""
        job_cards = self.get_job_cards()
        jobs = [CodementorJob.from_job_card(job_card) for job_card in job_cards]
        return jobs

    @screenshot_on_error()
    def update_job(self, job: 'CodementorJob'):
        """Update the job object with data from the job detail page."""
        logging.info(f'🆙 Updating job: {job.url} 🆙')
        while True:
            try:
                self.open_job(job, new_tab=True)
                job_detail_page_html = self.browser.page_source
                job.__dict__.update(job._parse_data_from_job_page(job_detail_page_html))
                break
            except:
                logging.error('🚨 Error updating job. Retrying... 🚨')
                time.sleep(job_detail_page.load_time)
        self.browser.close_tab()

    @screenshot_on_error()
    def apply(self, job: 'CodementorJob'):
        logging.info(f'🚀 Applying to job: {job.url} 🚀')
        self.open_job(job, new_tab=True)
        message = CAN_HELP_MESSAGE_TEMPLATE.format(client_name=job.client_first_name)
        self.send_job_interest(message)
        self.click_message_client_button()
        try:
            chatbox = self.find_chatbox(job.client_first_name)
            chatbox.send_message(message)

            # Set initial message to know what our first contact was.
            self.initial_message = message
        except Exception as e:
            self.browser.save_screenshot(build_screenshot_path())
            logging.error(f'🚨 Error sending message to client: {e} 🚨')
            logging.info(f'🚫 Skipping job: {job.url} 🚫')
        self.browser.close_tab()

    def send_job_interest(self, message):
        """Send a job interest message to the client."""
        self.fill_job_interest_textarea(message)
        self.click_job_interest_submit_button()    

    def fill_job_interest_textarea(self, message):
        textarea = self.browser.find_element('tag name', 'textarea')  
        textarea.click()
        self.browser.send_keys_with_emojis(textarea, message.replace('\n', ' '))
        textarea.send_keys(' ', Keys.BACKSPACE)  # For some reason, you need to add a key normally in order for their message box to validate.

    def click_job_interest_submit_button(self):
        """Click the submit button on the job detail page."""
        submit_button = self.browser.find_elements('tag name', 'button')[-2]
        submit_button.click()
        time.sleep(2)

    def click_message_client_button(self):
        """Click the message button on the job detail page."""
        message_button = self.browser.find_elements('tag name', 'button')[-2]
        message_button.click()
        time.sleep(3)  # Wait for the chatbox to load.

    @screenshot_on_error()
    def find_chatbox(self, name: str) -> 'Chatbox':
        """Find a chatbox by name."""
        chatboxes = self.get_chatboxes()
        for chatbox in chatboxes:
            if name in chatbox.name:
                logging.info(f'📬 Found chatbox for {name}! 📬')
                return chatbox
        raise ValueError(f'Could not find chatbox with name: {name}')

    def get_chatboxes(self) -> list['Chatbox']:
        """Get all current chatboxes currently open on the codementor site."""
        chatboxes = self.browser.find_elements('class name', '_3Qjjkp')
        return [Chatbox(chatbox, self.browser) for chatbox in chatboxes]

    def close_all_chatboxes(self):
        """Close all chatboxes currently open on the codementor site."""
        for chatbox in self.get_chatboxes():
            chatbox.close()

    @requires_page(related_job_list_page)
    def refresh_jobs(self):
        """Click the refresh button to view the newest jobs."""
        self.browser.scroll_to_top()
        while True:
            try:
                self.browser.implicitly_wait(5)
                refresh_button = self.browser.find_element('css selector', '.request-filter__refresh-btn')
                refresh_button.click()
                logging.info('🔄 Refreshed Jobs! 🔄')
                return
            except ElementClickInterceptedException:
                    self.close_popup()
            except NoSuchElementException:
                try:
                    logging.debug(f'3rd attempt at refresh on Current URL: {self.browser.url}')
                    self.browser.refresh()
                    logging.info('🌪️ Hard refreshed jobs! 🌪️')
                    logging.debug(f'🔄 Attempting to refresh normally 🔄')
                except Exception as e:
                    self.browser.driver.save_screenshot(build_screenshot_path())
                    logging.error(e)

    def close_popup(self):
        self.close_instant_help_request_popup()
        self.close_session_notice_popup()

    def close_instant_help_request_popup(self):
        try:
            instant_help_request_popup = self.browser.find_element('css selector', '.instant-help-enter-done')
            self.browser.remove_element(instant_help_request_popup)
            logging.info('💥🧨 Instant help popup destroyed! 🧨💥')
        except NoSuchElementException:
            logging.info('🔍 No instant help popup found. 🔍')
            pass

    def close_session_notice_popup(self):
        try:
            session_notice_popup = self.browser.find_element('css selector', '.session-notice')
            if session_notice_popup:
                self.browser.remove_element(session_notice_popup)
                logging.info('💥🧨 Session notice help popup destroyed! 🧨💥')
        except NoSuchElementException:
            logging.info('🔍 No session notice popup found. 🔍')
            pass


JOB_INFO_TEMPLATE = """\
Tags: {tags}
Title: {title}
Description: {description}
Label: {label}
Expected Budget: {expected_budget}
URL: {url}\
"""


@dataclass 
class CodementorJob(Job): 
    platform: str = Codementor.name
    title: str = ''
    read: bool = False
    tags: str = ''  # type: ignore
    label: str = ''
    expected_budget: str = ''

    def __str__(self):
        return JOB_INFO_TEMPLATE.format(**vars(self))

    @classmethod
    def from_job_card(cls, job_card_html: str | Tag):
        """Create a job object from a job card."""
        data = cls._parse_data_from_job_card(job_card_html)
        return cls(**data)

    @staticmethod
    def _parse_data_from_job_card(job_card_html: str | Tag):
        """Parse data from a job card."""
        soup = BeautifulSoup(str(job_card_html), 'html.parser')
        return {
            'url': Codementor.base_url + soup.find('a')['href'], # type: ignore
            'title': soup.find('span', class_='request-title__text').text,
            'read': soup.find('div', class_='dashboard__main-content-row--unread') is None,
            'label': soup.find('li', class_='content-row__header__label').text,
            'tags': ', '.join([tag.text for tag in soup.find_all('li', class_='content-row__header__tags-item')]),
        }

    @staticmethod
    def _parse_data_from_job_page(job_page_html: str | Tag) -> dict:
        soup = BeautifulSoup(str(job_page_html), 'html.parser')
        client_name = soup.find('a', class_='name').text
        title = soup.find('h2', class_='req-title').text
        description = soup.select_one('div.cui-md-viewer').text
        label = soup.find('span', class_='question-detail__type-label').text
        tags = ', '.join([tag.text for tag in soup.find_all('span', class_='question-detail__tags__item')])
        expected_budget = soup.find('b').text
        status = soup.find_all('b')[1].text
        publish_date = datetime.strptime(soup.find('time').text, '%b %d, %Y %I:%M %p')
        applied = soup.select_one('div.sc-1ro9pqn-1.kvjIuM').text == 'You\'ve expressed interest'
        return {
            'client_name': client_name,
            'title': title,
            'description': description,
            'label': label,
            'tags': tags,
            'expected_budget': expected_budget,
            'status': status,
            'publish_date': publish_date,
            'applied': applied,
        }

    def evaluate(self, manual: bool = False):
        if not manual:
            self.can_help = not self.contains_blocked_expertise()
            if self.can_help:
                logging.info(f'✅ Approved job: {self.url} ✅')
            else:
                logging.info(f'🚫 Blocked job: {self.url} 🚫')
            self.evaluation_method = 'automatic'
        else:
            self.can_help = input(f'{self}\n\nCan you help? (y/n): ').casefold() == 'y'
            self.evaluation_method = 'manual'


@dataclass
class Chatbox:
    chatbox: WebElement
    browser: Browser

    @property
    def name(self) -> str:
        """Get the name of the chatbox."""
        return self.chatbox.find_element('css selector', 'div._1eJvtL a').text

    def send_message(self, message: str):
        """Write a message in the chatbox."""
        self.write_message(message)
        self.send()

    def write_message(self, message: str):
        textarea = self.get_textarea()
        textarea.click()  # For some reason it's necessary to click before sending a message.
        self.browser.send_keys_with_emojis(textarea, message)
        textarea.send_keys(' ', Keys.BACKSPACE)  # For some reason you also need send a key in order for it to know there's a message.
        time.sleep(2)  # Wait for text to register.

    def send(self):
        """Send a message in the chatbox."""
        textarea = self.get_textarea()
        textarea.send_keys(Keys.ENTER)
        time.sleep(2)  # Wait for message send to register.

    def get_textarea(self) -> WebElement:
        """Get the textarea of the chatbox."""
        return self.chatbox.find_element('tag name', 'textarea')

    def close(self):
        """Close the chatbox."""
        close_button = self.chatbox.find_element('css selector', 'span._3e__zI')
        close_button.click()