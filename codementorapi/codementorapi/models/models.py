from __future__ import annotations

from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from typing import Optional
from pydantic import BaseModel, model_validator, ConfigDict, computed_field

from .base import IDURLModel
from codementorapi.constants import BASE_URL, FEATURED_REQUEST_STRING

BaseModel.model_config = ConfigDict(extra='forbid')


class LoginDetails(BaseModel):
    email: str
    password: str


class User(BaseModel):
    name: str = ''
    url: str = ''
    timezone: str = ''
    is_mentor: bool = False
    is_student: bool = False
    rate: int = 0
    messages: list[Message] = []

    @classmethod
    def from_request_details(cls, request_detail_html: str) -> User:
        soup = BeautifulSoup(request_detail_html, 'html.parser')
        user_name_link = soup.find('a', class_='name')
        url = user_name_link.get('href')
        name = user_name_link.text
        timezone = soup.find('div', 'tz').text
        return cls(name=name, url=url, timezone=timezone)


    @classmethod
    def from_chatbox(cls, chatbox_html: str) -> User:
        """Get the user that the chatbox is for."""
        soup = BeautifulSoup(chatbox_html, 'html.parser')
        user_name_link = soup.select_one('div._1eJvtL a')
        name = user_name_link.text
        url = user_name_link.get('href')
        timezone = soup.find('div', '_3CDOXy').text
        return User(name=name, url=url, timezone=timezone)
    

    @computed_field(alias='id')
    @property
    def username(self) -> str | None:
        return self.url.split('/')[-1] if self.url else None

    @computed_field
    @property
    def first_name(self) -> str:
        return self.name.split()[0]


class Job(BaseModel):
    total_amount: Optional[float] = None
    amount_earned: Optional[float] = None

    # Relationships
    request: Request
    details: Optional[FreelanceJob | Session] = None

    @computed_field
    @property
    def type(self) -> str:
        return self.request.type

    @computed_field
    @property
    def tags(self) -> list[str]:
        return self.request.tags

    @computed_field
    @property
    def review(self) -> Review | None:
        return self.details.review


class Request(IDURLModel):
    """Help requests posted on Codementor."""
    title: str
    is_read: bool
    is_featured: bool = False
    is_applied: bool = False
    tags: list[str] = []
    detail: str = ''
    posted_at: Optional[datetime] = None
    status: str = 'open'
    type: str = ''

    # Relationships
    user: Optional[User] = None
    expected_budget: ExpectedBudget = None

    @classmethod
    def from_request_card(cls, request_card_html: str) -> Request:
        soup = BeautifulSoup(request_card_html, 'html.parser')
        url = BASE_URL + soup.find('a').get('href')
        title = soup.find('span', class_='request-title__text').text.strip(FEATURED_REQUEST_STRING)
        is_featured = FEATURED_REQUEST_STRING in soup.find('div', class_='request-title').text
        is_read = soup.find('div', class_='dashboard__main-content-row--unread') is None
        request_type = soup.find('li', class_='content-row__header__label').text
        tags = [tag.text for tag in soup.select('li.content-row__header__tags-item')]
        expected_budget = ExpectedBudget.from_request_card(request_card_html)
        return cls(
            url=url,
            title=title,
            is_featured=is_featured,
            is_read=is_read,
            type=request_type,
            tags=tags,
            expected_budget=expected_budget,
        )

    @classmethod
    def from_request_details(cls, request_details_html: str, url: str):
        soup = BeautifulSoup(request_details_html, 'html.parser')
        user = User.from_request_details(request_details_html)
        title = soup.find('h2').text
        expected_budget = ExpectedBudget.from_request_details(request_details_html)
        detail = soup.find('div', class_='request-detail').text
        request_type = soup.find('span', class_='question-detail__type-label').text
        is_read = True
        tags = [tag_elem.text for tag_elem in soup.find_all('span', class_='question-detail__tags__item')]
        posted_at=datetime.strptime(soup.find('time').text, '%b %d, %Y %I:%M %p')
        return cls(
            url=url,
            user=user,
            title=title,
            expected_budget=expected_budget,
            detail=detail,
            type=request_type,
            is_read=is_read,
            tags=tags,
            posted_at=posted_at,
        )


class ExpectedBudget(BaseModel):
    amount: float
    type: str

    @classmethod
    def from_request_details(cls, request_details_html: str):
        soup = BeautifulSoup(request_details_html, 'html.parser')
        expected_budget_str = soup.find('div', class_='budget').text
        type = 'hourly' if 'hour' in expected_budget_str else 'fixed'
        amount = float(expected_budget_str.strip('US$').split()[0])
        return cls(amount=amount, type=type)

    @classmethod
    def from_request_card(cls, request_card_html: str):
        soup = BeautifulSoup(request_card_html, 'html.parser')
        expected_budget_str = soup.find('div', class_='content-row__budget').text
        amount = float(expected_budget_str.strip('$').strip('/hr').strip())
        type = 'hourly' if '/hr' in expected_budget_str else 'fixed'
        return cls(amount=amount, type=type)


class JobDetails(IDURLModel):
    user: Optional[User] = None
    total_amount: Optional[float] = None
    amount_earned: Optional[float] = None
    review: Optional[Review] = None


class Session(JobDetails):
    length: timedelta
    finished_at: datetime
    rate_per_15: Optional[int]

    @computed_field
    @property
    def started_at(self) -> datetime:
        return self.finished_at - self.length


class FreelanceJob(JobDetails):
    title: str
    description: Optional[None] = None


class Review(BaseModel):
    rating: int
    review: str
    user: User
    job_id: Optional[str] = None
    url: str


class Message(BaseModel):
    text: str
    sent_at: datetime
    user_id: str = None
    is_from_user: bool = None


class Application(BaseModel):
    user: User | None = None
    text: str
    sent_at: datetime
