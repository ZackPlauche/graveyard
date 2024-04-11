from elements import Element, Selector

from .common import LazyCardList
from codementorapi.models import FreelanceJob


class FreelanceJobCard(Element):
    selector = Selector(by='css selector', value='a.dashboard__offline-help-item')

    def scrape(self) -> FreelanceJob:
        soup = self.soup
        return FreelanceJob(
            url=self.get_attribute('href'),
            title=soup.find('div', class_='content-row__header__title').text,
            created_at=soup.select_one('.content-row__header .content-row__header__small').text.split('on')[1],
            total_amount=soup.find('div', class_='content-row__budget').text.strip('$'),
        )
    
    def has_review(self):
        return self.soup.find('div', class_='offline-help-item__no-review-label') is None


class FreelanceJobCardList(LazyCardList):
    item_element = FreelanceJobCard

    def get_freelance_jobs(self) -> list[FreelanceJob]:
        freelance_job_cards: list[FreelanceJobCard] = self.get_items()
        freelance_jobs = [card.scrape() for card in freelance_job_cards]
        return freelance_jobs
    
    def get_loaded_freelance_jobs(self) -> list[FreelanceJob]:
        freelance_job_cards: list[FreelanceJobCard] = self.get_loaded_items()
        freelance_jobs = [card.scrape() for card in freelance_job_cards]
        return freelance_jobs