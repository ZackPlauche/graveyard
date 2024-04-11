from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

BaseModel.model_config = ConfigDict(extra='forbid')


class Account(BaseModel):
    username: str
    password: str

    def login_info(self) -> tuple[str, str]:
        return self.username, self.password


class Student(BaseModel):
    id: str | None = None
    url: str | None = None
    name: str
    timezone: str | None = None
    grade_level: str | None = None
    payment_info_on_file: bool | None = None


class Job(BaseModel):
    id: str
    url: str
    topic: str
    subject: str | None
    description: str
    recommended_rate: int | None
    posted_at: datetime
    found_at: datetime
    student: Student
    application: Application | None = None


class Review(BaseModel):
    title: str
    body: str
    student_id: str
    job_id: str


class Application(BaseModel):
    rate: float
    message: str
    sent_at: datetime
    job_id: str | None = None


class Lesson(BaseModel):
    id: str
    url: str | None = None
    subject: str
    topic: str
    rate: float
    duration: int
    scheduled_at: datetime
    student_id: str
