from datetime import datetime

from selenium_objects import Element, Selector

from database.models import Session, User
from webscraper.utils import parse_time_str
from webscraper.constants import BASE_URL
from .common import LazyCardList


class SessionCard(Element):
    selector = Selector(by='css selector', value='a.dashboard__lesson-item')

    def scrape_session(self) -> Session:
        soup = self.soup
        url = BASE_URL + soup.find('a', class_='dashboard__lesson-item').get('href')
        user = User(name=soup.find('div', class_='content-row__header__title').text.split('with')[1].strip())
        length_str = soup.find('span', class_='dashboard__lesson-item__length').text
        length = parse_time_str(length_str)
        finished_at_str = soup.find('div', class_='content-row__finished-at').text
        finished_at = datetime.strptime(finished_at_str, '%b %d, %Y %I:%M %p')
        return Session(
            url=url,
            user=user,
            length=length,
            finished_at=finished_at,
        )
    
    def scrape_user(self) -> User:
        soup = self.soup
        name = soup.find('div', class_='content-row__header__title').text.split('with')[1].strip()
        url = BASE_URL + soup.find('a').get('href')
        return User(name=name, url=url)

    def refund_given(self):
        return self.soup.find('span', text='FULL REFUND') is not None


class SessionCardList(LazyCardList):
    """This element is needed for the weird scroll behavior of the session history page."""
    selector = Selector(by='xpath', value='/html/body/div[1]/div[5]/div[2]/div/div[2]/div[2]/div/div/div/div/div')
    item_element = SessionCard

    def get_sessions(self) -> list[Session]:
        session_cards: list[SessionCard] = self.get_items()
        sessions = [card.scrape_session() for card in session_cards]
        return sessions
    
    def get_loaded_sessions(self) -> list[Session]:
        session_cards: list[SessionCard] = self.get_loaded_items()
        sessions = [card.scrape_session() for card in session_cards]
        return sessions
