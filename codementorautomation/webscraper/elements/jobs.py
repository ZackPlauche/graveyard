import logging
import time
from datetime import datetime, timedelta

from selenium_objects import Element, Selector
from selenium.webdriver.common.keys import Keys

from database.models import Job, User
from webscraper.constants import BASE_URL, FEATURED_REQUEST_STRING
from .common import LazyCardList


class JobCard(Element):
    selector = Selector(by='css selector', value='a.dashboard__open-question-item')

    def scrape_job(self) -> Job:
        """Scrape the job data from the job card."""
        soup = self.soup
        url = BASE_URL + soup.find('a').get('href')
        title = soup.find('span', class_='request-title__text').text.strip(FEATURED_REQUEST_STRING)
        posted_at = self._scrape_posted_at()
        is_featured = FEATURED_REQUEST_STRING in soup.find('div', class_='request-title').text
        is_read = soup.find('div', class_='dashboard__main-content-row--unread') is None
        is_open = True  # Job is open if it's job card exists
        job_type = soup.find('li', class_='content-row__header__label').text
        tags = [tag.text for tag in soup.select('li.content-row__header__tags-item')]
        expected_budget_str = soup.find('div', class_='content-row__budget').text
        expected_budget = float(expected_budget_str.strip('$').strip('/hr').strip())
        expected_budget_type = 'hourly' if '/hr' in expected_budget_str else 'fixed'
        return Job(
            url=url,
            title=title,
            posted_at=posted_at,
            is_featured=is_featured,
            is_read=is_read,
            is_open=is_open,
            type=job_type,
            tags=tags,
            expected_budget=expected_budget,
            expected_budget_type=expected_budget_type,
        )

    def _scrape_posted_at(self) -> datetime:
        """Scrape the posted at time from the job card."""
        soup = self.soup
        posted_at_str = soup.find('div', class_='content-row__created-at').text
        if posted_at_str == 'a few seconds ago':
            posted_at = datetime.now()
        else:
            amount, unit, _ = posted_at_str.split()  # format: an hour ago, 3 months ago, etc.
            amount = 1 if amount in ['a', 'an'] else int(amount)
            if unit in 'minutes':
                posted_at = datetime.now() - timedelta(minutes=amount)
            elif unit in 'hours':
                posted_at = datetime.now() - timedelta(hours=amount)
            elif unit in 'days':
                posted_at = datetime.now() - timedelta(days=amount)
            elif unit in 'months':
                posted_at = datetime.now() - timedelta(days=amount * 30)
        return posted_at



class JobCardList(LazyCardList):
    """The list of job cards on the job list page."""
    item_element = JobCard


class JobDetails(Element):
    """The job details section of the job list page that contains most all of the job data."""
    selector = Selector(by='css selector', value='.question-detail')

    def scrape_job(self) -> Job:
        soup = self.soup
        user = self.scrape_user()
        title = soup.find('h2').text
        expected_budget_str = soup.find('div', class_='budget').text
        expected_budget = float(expected_budget_str.strip('US$').split()[0])
        expected_budget_type = 'hourly' if 'hour' in expected_budget_str else 'fixed'
        description = soup.find('div', class_='cui-md-viewer').text
        job_type = soup.find('span', class_='question-detail__type-label').text
        tags = [tag_elem.text for tag_elem in soup.find_all('span', class_='question-detail__tags__item')]
        posted_at=datetime.strptime(soup.find('time').text, '%b %d, %Y %I:%M %p')
        is_open = soup.find('div', class_='request-state').text == 'Open'
        return Job(
            user=user,
            title=title,
            expected_budget=expected_budget,
            expected_budget_type=expected_budget_type,
            description=description,
            type=job_type,
            tags=tags,
            posted_at=posted_at,
            is_open=is_open,
        )

    def scrape_user(self) -> User:
        """Parse the job details page to get the data of the user that posted the job."""
        soup = self.soup
        user_name_link = soup.find('a', class_='name')
        url = user_name_link.get('href')
        name = user_name_link.text
        timezone = soup.find('div', 'tz').text
        return User(name=name, url=url, timezone=timezone)

class JobInterestForm(Element):
    selector = Selector(by='css selector', value='.fVeJLb')

    @property
    def interest_message_sent(self) -> bool:
        """Check if the interest message has already been sent."""
        return bool(self.soup.find('div', text="You've expressed interest"))

    @property
    def interest_message(self) -> str | None:
        """Get the text of the interest message that was sent."""
        return self.soup.find('div', class_='message').text.strip('"')

    def send_interest_message(self, message: str):
        """Send the interest message."""
        if self.interest_message_sent:
            raise Exception('Interest message already sent. Cannot send another interest message.')
        self._write_message(message)
        self._click_submit()

    def click_message_client_button(self):
        """Click the message client """
        if not self.interest_message_sent:
            raise Exception('Interest message not sent. Cannot click message client button until interest message is sent.')
        message_client_button = self.find_element('tag name', 'button')
        message_client_button.click()
        time.sleep(3)  # Wait for chatbox to load.

    def _write_message(self, message: str):
        if self.interest_message_sent:
            raise Exception('Interest message already sent. Cannot send another interest message.')
        textarea = self.find_element('tag name', 'textarea')
        textarea.click()  # For some reason it's necessary to click before sending a message.
        textarea.send_keys_with_emojis(message)
        textarea.send_keys(' ', Keys.BACKSPACE)  # For some reason, you need to add a key normally in order for their message box to validate.

    def _click_submit(self):
        if self.interest_message_sent:
            raise Exception('Interest message already sent. Cannot send another interest message.')
        submit_button = self.find_element('tag name', 'button')
        submit_button.click()
        time.sleep(2)


class RefreshJobsButton(Element):
    """The refresh button on the job list page."""
    selector = Selector(by='css selector', value='.request-filter__refresh-btn')

    def click(self):
        """Bring the refresh button into view and click on it."""
        self.driver.execute_script('window.scrollTo(0, 0);', self.element)
        self.element.click()
        logging.debug('🖱️ Clicked RefreshButton')
