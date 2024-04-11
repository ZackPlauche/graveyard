import os
from typing import Self

from pydantic import BaseModel, ConfigDict
from selenium.webdriver.remote.webdriver import WebDriver

from .models import LoginDetails, Session, FreelanceJob, Request
from .pages import LoginPage, OpenRequestsPage, SessionHistoryPage, FreelanceJobsPage, Dashboard, RequestDetailPage


class CodementorAPI(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    login_details: LoginDetails
    driver: WebDriver

    @classmethod
    def start(cls, driver: WebDriver):
        codementor = cls.from_env(driver=driver)

        # If not already logged in, login
        Dashboard.bring(driver)
        if not codementor.driver.current_url == Dashboard.url:
            codementor.login()

        return codementor

    @classmethod
    def from_env(cls, driver: WebDriver) -> Self:
        email = os.getenv('CODEMENTOR_EMAIL')
        password = os.getenv('CODEMENTOR_PASSWORD')
        if all([email, password]):
            login_details = LoginDetails(email=email, password=password)
        else:
            raise Exception('Login details not found in environment variables.')
        return cls(login_details=login_details, driver=driver)

    def login(self):
        """Login to Codementor."""  # TODO: Add handler for reCaptcha popup
        LoginPage.bring(self.driver).login(login_details=self.login_details)

    def get_open_requests(self) -> list[Request]:
        """Get all open requests on the Open Requests page."""
        request_cards = OpenRequestsPage.bring(self.driver).get_request_cards()
        open_requests = [Request.from_request_card(request_card.html) for request_card in request_cards]
        return open_requests

    def update_request_details(self, request: Request) -> Request:
        """Update the details of a request."""
        request_details = RequestDetailPage.bring(self.driver, instance=request).get_request_details()
        request_with_details = Request.from_request_details(request_details.html, url=request.url)
        request.__dict__.update(request_with_details.__dict__)
        return request

    def apply_to_request(self, request: Request, message: str) -> None:
        """Apply to a request."""
        RequestDetailPage.bring(self.driver, instance=request).apply(message=message)

    # ------------------------------------------------------------------------------ Don't focus on right now #
    def get_session_list_data(self) -> list[Session]:
        """Get all sessions on the Session list page."""
        session_history_page = SessionHistoryPage.bring(driver=self.driver)
        sessions = session_history_page.get_sessions()
        return sessions

    def get_freelance_jobs(self) -> list[FreelanceJob]:
        freelance_jobs_page = FreelanceJobsPage.bring(driver=self.driver)
        freelance_jobs = freelance_jobs_page.get_freelance_jobs()
        return freelance_jobs
