from __future__ import annotations

from typing import Self
# import sorteddict

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Text, exists, asc
from sqlalchemy.orm import relationship, backref, Query, Session as DBSession
from sqlalchemy_utils import URLType, ChoiceType, JSONType

from .basemodel import BaseModel, Base
from .choices import JobType, ExpectedBudgetType, UserType


class Expertise(BaseModel):
    """Expertise or blacklisted expertise of a mentor to determine which jobs 
    that mentor can help with.
    """
    name = Column(String(255), nullable=False, unique=True)
    is_blacklisted = Column(Boolean, default=False)
    is_whitelisted = Column(Boolean, default=False)

    def __str__(self):
        return self.name
        
    @classmethod
    def query(cls, session: DBSession) -> Query[Self]:
        """Expertise by default should be ordered by name in ascending order."""
        return super().query(session).order_by(asc(Expertise.name))

    @classmethod
    def get_blacklist(cls, session: DBSession) -> list[str]:
        """Get all blacklisted expertise."""
        return [str(expertise) for expertise in cls.get_blacklisted(session)]

    @classmethod
    def get_blacklisted(cls, session: DBSession) -> Query[Expertise]:
        """Get all blacklisted expertise."""
        return cls.filter_by(session, is_blacklisted=True)
    
    
    @classmethod
    def get_whitelist(cls, session: DBSession) -> list[str]:
        """Get all whitelisted expertise."""
        return [str(expertise) for expertise in cls.get_whitelisted(session)]
    
    @classmethod
    def get_whitelisted(cls, session: DBSession) -> Query[Expertise]:
        """Get all whitelisted expertise."""
        return cls.filter_by(session, is_whitelisted=True)
    
    @classmethod
    def get_unlisted(cls, session: DBSession) -> Query[Expertise]:
        """Get all unlisted expertise."""
        return cls.filter_by(session, is_whitelisted=False, is_blacklisted=False)

    @classmethod
    def get_expertise(cls, session: DBSession) -> Query[Expertise]:
        """Get non-blacklisted expertise."""
        return cls.filter_by(session, is_blacklisted=False)
    
    @classmethod
    def load_from_job_tags(cls, session: DBSession, jobs: list[Job] = None) -> list[Expertise]:
        """Load expertise from existing job tags."""
        if not jobs:
            jobs = Job.all(session)
        all_tags = set([tag for job in jobs for tag in job.tags])
        expertise_names = [str(expertise) for expertise in cls.all(session)]
        new_expertise = [Expertise(name=tag) for tag in all_tags if tag not in expertise_names]
        session.add_all(new_expertise)
        session.commit()
        return new_expertise


class User(BaseModel):
    """Codementor User (typically a customer)"""
    url = Column(URLType, nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    timezone = Column(String(255), nullable=True)
    is_mentor = Column(Boolean, default=False)
    is_student = Column(Boolean, default=False)
    current_rate = Column(Integer, default=0)

    @property
    def first_name(self) -> str:
        name: str = self.name
        return name.split()[0] if name else ''

    def exists(self, session: DBSession) -> bool:
        """Determine if the user exists in the database."""
        return session.query(exists().where(User.url == self.url)).scalar()


class Job(BaseModel):
    """A job posting on Codementor."""
    url = Column(URLType, nullable=False, unique=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default='', comment='The details of the job.')
    tags = Column(JSONType, nullable=False, default=[])
    posted_at = Column(DateTime, nullable=True, default=None)
    type = Column(ChoiceType(choices=JobType), nullable=False)
    expected_budget = Column(Integer, nullable=True)
    expected_budget_type = Column(ChoiceType(choices=ExpectedBudgetType), nullable=False)

    # Flags
    is_open = Column(Boolean, default=True, comment='Whether the job is still open or not.')
    is_read = Column(Boolean, default=False, comment='Whether the job has been read by the bot')
    is_featured = Column(Boolean, default=False, comment='Whether the customer has paid to feature the job. Important to know because that means they have the money afforded to feature it and are highly invested in finding quality help.')
    is_applied_to = Column(Boolean, default=False, comment='Whether or not the job has already been applied to.')
    is_fully_updated = Column(Boolean, default=False, comment='Whether or not the job has been fully updated with the latest information from the job details page.')
    is_ignored = Column(Boolean, default=False, comment='Whether or not the job should be ignored by the bot.')
    can_help = Column(Boolean, default=None, nullable=True, comment='Whether or not the job can be helped by a mentor.')

    # Foreign Keys
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    # Relationships
    user = relationship('User', backref=backref('job_requests', lazy=True))

    def __str__(self):
        return self.title

    @classmethod
    def query(cls, session: DBSession) -> Query[Self]:
        """Base query for jobs that ignores jobs that have been ignored."""
        return super().query(session).filter(Job.is_ignored.is_not(True))
    
    @classmethod
    def get_applicable(cls, session: DBSession) -> Query[Self]:
        """Get all jobs that can be applied to. Job must be:
        1. Open (Not closed)
        2. Fully updated (to know that it's applied to)
        3. Not already applied to.
        4. Should contain a user
        5. Should be able to be helped already
        Arguably it should be evaluated by now, but in case it's not we'll evaluate it later.
        """
        return cls.filter(session,
            Job.user_id.is_not(None),
            Job.can_help == True,
            Job.is_applied_to == False,
            Job.is_open == True,
            Job.is_fully_updated == True
        ).all()
    
    @classmethod
    def get_most_popular_tags(cls, session: DBSession) -> list[tuple[str, int]]:
        """Get most popular tags from all jobs sorted by count in ascending order"""
        tags = {tag: 0 for tag in cls.get_unique_tags(session)}
        for job in cls.all(session):
            for tag in job.tags:
                tags[tag] += 1
        return sorted(tags.items(), key=lambda item: item[1], reverse=True)

    @classmethod
    def get_unique_tags(cls, session: DBSession) -> list[str]:
        """Get all tags from all jobs."""
        return list({tag for job in cls.all(session) for tag in job.tags})

    def contains_blacklisted_tags(self, blacklist: list[str]) -> bool:
        """Determine if the job contains any blacklisted tags."""
        tags_in_blacklist = [tag for tag in self.tags if tag in blacklist]
        return bool(tags_in_blacklist)

    def evaluate(self, session: DBSession, blacklist: list[str] = None) -> bool:
        """Evaluate the job to determine if it can be helped by a mentor."""
        if not blacklist:
            blacklist = Expertise.get_blacklist(session)
        self.can_help = not self.contains_blacklisted_tags(blacklist)
        return self.can_help

    @classmethod
    def evaluate_list(cls, session: DBSession, jobs: list[Job], blacklist: list[str] = None) -> list[Job]:
        """Evaluate a list of jobs."""
        if not blacklist:
            blacklist = Expertise.get_blacklist(session)
        for job in jobs:
            job.evaluate(session, blacklist)
        session.add_all(jobs)
        return jobs

    @classmethod
    def evaluate_all(cls, session: DBSession, blacklist: list[str] = None) -> bool:
        """Evaluate all jobs in the database."""
        if not blacklist:
            blacklist = Expertise.get_blacklist(session)
        jobs = cls.all(session)
        cls.evaluate_list(session, jobs, blacklist)
        return jobs

    def is_applicable(self):
        """Determine if the job is applicable to be helped by a mentor."""
        return bool(self.user) and self.is_open and self.can_help and not self.is_applied_to


class Review(BaseModel):
    """A review that a user left for a job."""
    url = Column(URLType, nullable=False, unique=True, comment='The URL where the review can be found.')
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    
    user = relationship(User, backref=backref('reviews', lazy=True))
    job = relationship(Job, backref=backref('reviews', lazy=True))


class Session(BaseModel):
    """A session between a mentor and a student."""
    length = Column(Integer, nullable=False, comment='The length of the session in seconds.')
    finished_at = Column(DateTime, nullable=False, comment='The time the session was finished.')
    rate = Column(Integer, nullable=False, comment='The rate per 15 minutes.')
    cost = Column(Integer, nullable=False, comment='The total cost of the session.')
    amount_earned = Column(Integer, nullable=False, comment='The total amount earned from the session.')

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    review_id = Column(Integer, ForeignKey('review.id'), nullable=True)
    
    user = relationship(User, backref=backref('sessions', lazy=True))
    job = relationship(Job, backref=backref('session', lazy=True, uselist=False))
    review = relationship(Review, backref=backref('session', lazy=True, uselist=False))

    @property
    def started_at(self) -> datetime:
        return self.finished_at - self.length


class FreelanceJob(BaseModel):
    """A freelance completed job."""
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default='', comment='The details of the job.')
    cost = Column(Integer, nullable=False, comment='The total cost of the session.')
    amount_earned = Column(Integer, nullable=False, comment='The total amount earned from the session.')

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    review_id = Column(Integer, ForeignKey('review.id'), nullable=True)

    user = relationship(User, backref=backref('freelance_jobs', lazy=True))
    job = relationship(Job, backref=backref('freelance_job', lazy=True, uselist=False))
    review = relationship('Review', backref=backref('freelance_job', lazy=True, uselist=False))


class Message(BaseModel): 
    text = Column(Text, nullable=False, default='')
    sent_at = Column(DateTime, nullable=False, comment='The time the message was sent.')
    sent_by = Column(ChoiceType(choices=UserType), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship(User, backref=backref('messages', lazy=True))


class Application(BaseModel): 
    """An application to a job."""
    message = Column(Text, nullable=False, default='')
    sent_at = Column(DateTime, nullable=False, comment='The time the application was sent.')

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)

    user = relationship(User, backref=backref('applications', lazy=True))
    job = relationship(Job, backref=backref('application', lazy=True, uselist=False))