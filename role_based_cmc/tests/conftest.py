import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.database import Base
from app.core.config import settings


TEST_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db_session():
    db_test :Session = TestingSessionLocal()
    try:
        yield db_test
    finally:
        db_test.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            db_test.execute(table.delete())
        db_test.commit()
        db_test.close()
