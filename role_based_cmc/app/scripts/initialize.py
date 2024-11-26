from app.core.database import SessionLocal
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.roles_service import RoleService
from app.services.user_service import UserService


def initialize_data():
    session = SessionLocal()
    role_repository=RoleRepository(session)
    role_service = RoleService(role_repository)
    user_repository = UserRepository(session)
    user_service = UserService(user_repository,role_repository)

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
        session.close()  # Ensure session is closed
