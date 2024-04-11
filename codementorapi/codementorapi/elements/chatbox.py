import time
from typing import Self
from datetime import datetime

from elements import Element, Selector
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from codementorapi.models import Request, User, Message


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

    def send_message(self, message: str):
        textarea = self.find_element('tag name', 'textarea')
        textarea.click()  # For some reason it's necessary to click before sending a message.
        textarea.send_keys_with_emojis(message)
        textarea.send_keys(' ', Keys.BACKSPACE)  # For some reason, you also need to send a key in order for it to know there's a message.
        time.sleep(2)  # Wait for text to register
        textarea.send_keys(Keys.ENTER)
        time.sleep(2)  # Wait for message send to register.

    def get_messages(self):
        # TODO: Load all messages first
        messages = []
        for message_element in self.find_elements('css selector', 'div._3Q6MKh'):
            soup = message_element.soup
            message = Message(
                user=self.user if soup.find('a') else None,
                text=soup.text,
                send_at=datetime.strptime(soup.find('div').get('title'), '%b %d, %Y %I:%M %p')
            )
            messages.append(message)
        return messages

    def close(self):
        """Close the chatbox."""
        close_button = self.find_element('css selector', 'button._3e__zI')
        close_button.click()

    @property
    def user(self) -> User:
        """Get the user that the chatbox is for."""
        return User.from_chatbox(self.html)
    
    @property
    def related_request(self) -> Request:
        try:
            related_request_box = self.find_element('css selector', 'div.DOwz8r')
            soup = related_request_box.soup
            return Request(
                url=soup.find('a', '_3DgTZq').get('href'),
                title=soup.find('div', '_1GjOeY').text,
            )
        except:
            return None
