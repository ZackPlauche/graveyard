import time
from datetime import datetime

from elements import Element, Selector
from selenium.webdriver.common.keys import Keys

from .common import LazyCardList
from codementorapi.models import Request, User, ExpectedBudget
from codementorapi.constants import BASE_URL, FEATURED_REQUEST_STRING


class RequestCard(Element):
    selector = Selector(by='css selector', value='a.dashboard__open-question-item')

    def scrape(self) -> Request:
        soup = self.soup
        title = soup.find('div', class_='content-row__header__title').text
        expected_budget_str = soup.find('div', class_='content-row__budget').text
        expected_budget = ExpectedBudget.from_str(expected_budget_str)
        print(expected_budget)
        return Request(
            url=BASE_URL + soup.find('a').get('href'),
            title=title.strip(FEATURED_REQUEST_STRING),
            featured=title.startswith(FEATURED_REQUEST_STRING),
            read=soup.find('div', class_='dashboard__main-content-row--unread') is None,
            label=soup.find('li', class_='content-row__header__label').text,
            tags=[tag.text for tag in soup.select('li.content-row__header__tags-item')],
            expected_budget=expected_budget,
        )


class RequestCardList(LazyCardList):
    """This element is needed for the weird scroll behavior of the session history page."""
    item_element = RequestCard


class RequestDetails(Element):
    selector = Selector(by='css selector', value='.question-detail')


class RequestInterestForm(Element):
    selector = Selector(by='css selector', value='.fVeJLb')

    @property
    def interest_message_sent(self) -> bool:
        return bool(self.soup.find('div', text="You've expressed interest"))

    def send_interest_message(self, message: str):
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
