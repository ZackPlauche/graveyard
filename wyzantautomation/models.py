from typing import Callable
from datetime import datetime
from pydantic import BaseModel
from wyzantapi.models import Job as WyzantJob, Application

class Strategy(BaseModel):
    """Strategy to determine which pricing should be used based on automation base settings."""
    name: str
    description: str | None
    function: Callable


class Job(WyzantJob):
    received_reply: bool
    replied_at: datetime | None = None


class Application(Application):
    """Application to be sent to the student."""
    strategy: Strategy


class MessageTemplate(BaseModel):
    """Message template to be used in the automation."""
    name: str
    template: str
    description: str | None = None

    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)


class AutomationError(BaseModel):
    screenshot_path: str
    url: str
    message: str

    def __str__(self):
        return f"""\
--------------------
NEW AUTOMATION ERROR
--------------------
URL: {self.url}
Screenshot: {self.screenshot_path}
Error Message: {self.message}\
"""