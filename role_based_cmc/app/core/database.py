from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import psycopg2.errors
import os

DATABASE_URL="postgresql://postgres:root@localhost/cms_role_based"
DB_NAME = "cms_role_based"
DB_USER = "postgres"
DB_PASSWORD = "root"
DB_HOST = "localhost"



# Ensure the database exists
def create_database_if_not_exists():
    try:

        connection = psycopg2.connect(
            dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        connection.autocommit = True
        cursor = connection.cursor()


        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cursor.fetchone()
        if not exists:

            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database {DB_NAME} created successfully!")
        else:
            print(f"Database {DB_NAME} already exists.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while creating database: {e}")



create_database_if_not_exists()

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
