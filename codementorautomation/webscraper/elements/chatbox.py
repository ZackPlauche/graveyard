import time
from typing import Self
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium_objects import Element, Selector

from database.models import User, Message, Job
from webscraper.constants import BASE_URL


class Chatbox(Element):
    selector = Selector(by='css selector', value='._3Qjjkp')

    @classmethod
    def find_by_user(cls, driver, user: User) -> Self:
        """Find a chatbox by the user that it's for."""
        try:
            chatbox = [chatbox for chatbox in cls.find_all(driver) if chatbox.user.name == user.name][0]
            return chatbox
        except:
            raise NoSuchElementException(f'Chatbox for user {user} not found.')

    @property
    def user(self) -> User:
        """Get the user that the chatbox is for."""
        return self.scrape_user()

    def scrape_user(self) -> User:
        """Parse the chatbox to get the data of the user that posted the job."""
        soup = self.soup
        user_name_link = soup.select_one('div._1eJvtL a')
        name = user_name_link.text
        url = user_name_link.get('href')
        timezone = soup.find('div', '_3CDOXy').text
        return User(name=name, url=url, timezone=timezone)

    def send_message(self, message: str):
        """Write and send a message in the chatbox."""
        textarea = self.find_element('tag name', 'textarea')
        textarea.click()  # For some reason it's necessary to click before sending a message.
        textarea.send_keys_with_emojis(message)
        textarea.send_keys(' ', Keys.BACKSPACE)  # For some reason, you also need to send a key in order for it to know there's a message.
        time.sleep(2)  # Wait for text to register
        textarea.send_keys(Keys.ENTER)
        time.sleep(2)  # Wait for message send to register.

    # def get_messages(self):
    #     # TODO: Load all messages first
    #     messages = []
    #     for message_element in self.find_elements('css selector', 'div._3Q6MKh'):
    #         soup = message_element.soup
    #         message = Message(
    #             user=self.user if soup.find('a') else None,
    #             text=soup.text,
    #             send_at=datetime.strptime(soup.find('div').get('title'), '%b %d, %Y %I:%M %p')
    #         )
    #         messages.append(message)
    #     return messages

    def close(self):
        """Close the chatbox."""
        close_button = self.find_element('css selector', 'button._3e__zI')
        close_button.click()

    # @property
    # def job(self) -> Job | None:
    #     """Get the job that the chatbox is for if there is a related job, 
    #     otherwise return None."""
    #     return self.scrape_job()

    # def scrape_job(self) -> Job | None:
    #     """Parse the chatbox to get the data of the related job that the chatbox 
    #     is for if there is a related job, otherwise return None."""
    #     soup = self.soup
    #     related_request_box = soup.find('div', class_='DOwz8r')
    #     url = BASE_URL + related_request_box.find('a').get('href')
    #     title = related_request_box.find('div', class_='_1GjOeY').text
    #     return Job(url=url, title=title)
