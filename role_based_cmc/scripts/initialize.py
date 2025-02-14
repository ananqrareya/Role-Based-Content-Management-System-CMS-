

import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.core.database import SessionLocal, engine
from app.core.database import get_db
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.roles_service import RoleService
from app.services.user_service import UserService
from app.core.config import settings
import psycopg2
import psycopg2.errors


def create_database_if_not_exists():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {settings.DB_NAME}")
            print(f"Database {settings.DB_NAME} created successfully!")
        else:
            print(f"Database {settings.DB_NAME} already exists.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while creating database: {e}")

def initialize_data():
    create_database_if_not_exists()

    session = SessionLocal()
    role_service = RoleService(session)
    user_service = UserService(session)

    try:
        role_service.create_role_if_not_exists("Admin")
        role_service.create_role_if_not_exists("Editor")
        role_service.create_role_if_not_exists("Reader")
        user_service.create_admin_user(
            email="admin@example.com",
            username="admin",
            password="Admin@123",
            role_name="Admin"
        )
        print("Default roles and admin user initialized.")
    except Exception as e:
        print(f"Error during initialization: {e}")
    finally:
        session.close()

create_database_if_not_exists()
initialize_data()
