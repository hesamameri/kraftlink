# dependencies.py
from .database import database
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
