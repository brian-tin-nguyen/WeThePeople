'''
Without this the app has no memory. everytime it restarts, the data is gone.
database.py helps connects app to real DB.

# Tells SQLAlchemy WHERE the database is

install sqlalchemy: uv add sqlalchemy asyncpg
'''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Tell SQLAlchemy WHERE the database file is
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/wethepeople")

# This Create the "engine" (actual connection to the DB)
engine = create_engine(DATABASE_URL)

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