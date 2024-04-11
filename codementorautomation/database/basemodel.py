from typing import Self
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, exists
from sqlalchemy.orm import declarative_base, DeclarativeMeta, Session, Query

from .utils import title_to_snake

Base: DeclarativeMeta = declarative_base()


class BaseModel(Base):
    """Base model for all models to keep basic metadata and conveniences methods."""
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init_subclass__(cls, **kwargs):
        """Set the table name to the snake case version of the class name."""
        super().__init_subclass__(**kwargs)
        cls.__tablename__ = title_to_snake(cls.__name__)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
    
    def __iter__(self):
        for column in self.__table__.columns:
            yield column.name, getattr(self, column.name)
    
    def to_dict(self) -> dict[str, any]:
        return dict(self)
    
    def update(self, other: Self) -> Self:
        """Update the model with the given keyword arguments."""
        for key, value in dict(other).items():
            if value is not None:
                setattr(self, key, value)
        return self

    def add(self, session: Session) -> Self:
        """Add the model to the database."""
        session.add(self)
        return self

    def create(self, session: Session) -> Self:
        """Create the model in the database."""
        session.add(self)
        session.commit()
        return self

    @classmethod
    def query(cls, session: Session) -> Query[Self]:
        """Query the model."""
        return session.query(cls)
    
    @classmethod
    def filter(cls, session: Session, *criterion) -> Query[Self]:
        """Filter the model."""
        return cls.query(session).filter(*criterion)
    
    @classmethod
    def filter_by(cls, session: Session, **kwargs) -> Query[Self]:
        """Filter the model by the given keyword arguments."""
        return cls.query(session).filter_by(**kwargs)

    @classmethod
    def all(cls, session: Session) -> list[Self]:
        """Get all instances of the model."""
        return cls.query(session).all()

    @classmethod
    def get(cls, session: Session, **kwargs) -> Self:
        """Get the first instance a model by the given keyword arguments."""
        return cls.query(session).filter_by(**kwargs).first()

    def delete(self, session: Session) -> Self:
        """Delete the model from the database."""
        session.delete(self)
        session.commit()
        return self
    
    @classmethod
    def delete_all(cls, session: Session, confirm: bool = True) -> None:
        """Delete all instances of the model from the database."""
        if confirm:
            confirm: str = input(f'Are you sure you want to delete all {cls.__name__}? (y/N): ')
            if confirm.lower() != 'y':
                print('Aborting.')
                return
        cls.query(session).delete()
        session.commit()

    def exists(self, session: Session, *criterion) -> bool:
        """Check if an instance exists."""
        return session.query(exists().where(*criterion)).scalar()
    
    @classmethod
    def count(cls, session: Session):
        """Count the number of instances of the model."""
        return cls.query(session).count()