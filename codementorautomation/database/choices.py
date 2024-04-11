from enum import Enum


class JobType(Enum):
    ONE_ON_ONE = '1:1 live help'
    LONGTERM = 'Long-term'
    FREELANCE_JOB = 'Freelance job'
    CODE_REVIEW = 'Code review'


class ExpectedBudgetType(Enum):
    FIXED = 'fixed'
    HOURLY = 'hourly'


class UserType(Enum):
    MENTEE = 'mentee'
    MENTOR = 'mentor'