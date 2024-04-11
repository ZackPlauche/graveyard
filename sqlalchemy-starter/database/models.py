from sqlalchemy import Column, Integer, String, DateTime, Integer
from sqlalchemy.orm import relationship, backref, Query, Session
from sqlalchemy_utils import EmailType, URLType, JSONType, UUIDType, ChoiceType, PasswordType, PhoneNumberType

from .basemodel import BaseModel, Base


# Create your models here