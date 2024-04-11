from selenium_objects import Element, Selector

from database.models import FreelanceJob
from webscraper.constants import BASE_URL
from .common import LazyCardList


class FreelanceJobCard(Element):
    selector = Selector(by='css selector', value='a.dashboard__offline-help-item')

    def scrape_freelance_job(self) -> FreelanceJob:
        soup = self.soup
        url = BASE_URL + soup.find('a').get('href')
        title = soup.find('div', class_='content-row__header__title').text
        created_at = soup.select_one('.content-row__header .content-row__header__small').text.split('on')[1]
        total = soup.find('div', class_='content-row__budget').text.strip('$')
        return FreelanceJob(url=url, title=title, created_at=created_at, total=total)
    
    def has_review(self):
        return self.soup.find('div', class_='offline-help-item__no-review-label') is None


class FreelanceJobCardList(LazyCardList):
    item_element = FreelanceJobCard

    def get_freelance_jobs(self) -> list[FreelanceJob]:
        freelance_job_cards: list[FreelanceJobCard] = self.get_items()
        freelance_jobs = [card.scrape_freelance_job() for card in freelance_job_cards]
        return freelance_jobs
    
    def get_loaded_freelance_jobs(self) -> list[FreelanceJob]:
        freelance_job_cards: list[FreelanceJobCard] = self.get_loaded_items()
        freelance_jobs = [card.scrape_freelance_job() for card in freelance_job_cards]
        return freelance_jobs