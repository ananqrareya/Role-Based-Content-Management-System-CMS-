from sqlalchemy.orm import Session

from app.core.database_config import SessionLocal, engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_db():
    db :Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
