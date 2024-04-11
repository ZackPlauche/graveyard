from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from proposal_sender.settings import EXPERTISE_BLACKLIST
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .platforms.base import Platform


JOB_INFO_TEMPLATE = """\
Description: {description}
URL: {url}\
"""


@dataclass
class Job(ABC):
    url: str
    platform: str = ''
    client_name: str = ''
    description: str = ''
    can_help: bool | None = None
    evaluation_method: str = ''
    status: str = ''
    publish_date: datetime | None = None
    applied: bool = False
    initial_message: str = ''
    full_data: bool = False
    
    def __str__(self):
        return JOB_INFO_TEMPLATE.format(**vars(self))

    @property
    def client_first_name(self) -> str:
        """Return the client's first name."""
        return self.client_name.split(' ')[0]

    def update(self, data: dict):
        """Update the job with new data."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {**vars(self)}

    @abstractmethod
    def evaluate():
        pass

    def contains_blocked_expertise(self) -> bool:
        """Determine if the job contains any blocked expertise."""
        return any(expertise.lower() in str(self).lower() for expertise in EXPERTISE_BLACKLIST)

