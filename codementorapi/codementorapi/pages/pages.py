from codementorapi.elements import FreelanceJobCardList, SessionCardList
from codementorapi.models import Session
from codementorapi.models import FreelanceJob

from .base import BasePage


class Dashboard(BasePage):
    url = 'https://www.codementor.io/m/dashboard'


class FreelanceJobsPage(BasePage):
    url = 'https://www.codementor.io/m/dashboard/offline-help?type=solved'

    def get_freelance_jobs(self) -> list[FreelanceJob]:
        return FreelanceJobCardList.find(self.driver).get_freelance_jobs()


class SessionHistoryPage(BasePage):
    url = 'https://www.codementor.io/m/dashboard/session-history'

    def get_sessions(self) -> list[Session]:
        """Get all sessions on the page."""
        return SessionCardList.find(self.driver).get_sessions()

    def get_loaded_sessions(self) -> list[Session]:
        """Get sessions that are currently loaded on the page."""
        return SessionCardList.find(self.driver).get_loaded_sessions()
