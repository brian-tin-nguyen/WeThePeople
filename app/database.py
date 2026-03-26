'''
Without this the app has no memory. everytime it restarts, the data is gone.
database.py helps connects app to real DB.

Start SQLite then switch PostgreSQL later

install sqlalchemy: uv add sqlalchemy asyncpg
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Tell SQLAlchemy WHERE the database file is
DATABASE_URL = "sqlite:///./wethepeople.db"

# This Create the "engine" (actual connection to the DB)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# This is where we create a session factory a "session" is like a temporary workspace
#    where you make changes before saving them to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class models will inherit from this
class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()