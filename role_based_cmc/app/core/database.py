
from app.core.database_config import SessionLocal, engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
