from settings import BASE_DIR

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

db_url = 'sqlite:///' + str(BASE_DIR / 'db.sqlite3')

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)