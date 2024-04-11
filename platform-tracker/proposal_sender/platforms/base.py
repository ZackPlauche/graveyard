from abc import ABC, abstractmethod

from browsers import Browser
from browsers.pages import Page
from proposal_sender.base_job import Job

from decouple import config


class Platform(ABC):
    detail_page: Page = Page('')
    login_page: Page = Page('')

    @classmethod
    @property
    def name(cls) -> str:
        return cls.__name__

    def __init__(self, browser: Browser, evaluate_manually: bool = False, login_info: dict[str, str] = None):  # type: ignore
        """Initialize a platform."""
        self.browser = browser
        self.evaluate_manually = evaluate_manually
        self.login_info = login_info

    def __str__(self):
        return self.name

    @abstractmethod
    def autopilot(self):
        pass

    @abstractmethod
    def send_proposals(self):
        pass

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def get_jobs(self) -> list[Job]:
        pass

    @abstractmethod
    def apply(self, job):
        pass

    def open_job(self, job: 'Job', new_tab: bool = False):
        """Open a job's detail page."""
        self.browser.open_page(self.detail_page.with_url(job.url), new_tab=new_tab)

    @classmethod
    def get_login_info(cls) -> tuple[str, str]:
        """Get login info from environment variables."""
        username = config(f'{cls.name.upper()}_USERNAME')
        password = config(f'{cls.name.upper()}_PASSWORD')
        return (username, password)  # type: ignore