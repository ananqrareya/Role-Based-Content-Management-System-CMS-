import bcrypt
from fastapi import HTTPException

from app.models.User import User
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.user_schema import RegisterRequest


class UserService:
    def __init__(
        self, user_repository: UserRepository, role_repository: RoleRepository
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def create_admin_user(
        self, email: str, username: str, password: str, role_name: str
    ):

        if self.user_repository.get_user_by_email(email):
            raise ValueError(f"Email '{email}' already exists")

        role = self.role_repository.get_role_by_name(role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' does not exist")

        hashed_password = self.hash_password(password)
        admin_user = User(
            email=email, username=username, password=hashed_password,
            role_id=role.id
        )
        return self.user_repository.create_user(admin_user)

    def register_user(self, user: RegisterRequest):
        if self.user_repository.get_user_by_email(user.email):
            raise ValueError(f"Email '{user.email}' already exists")
        if self.user_repository.get_user_by_username(user.username):
            raise ValueError(f"Username '{user.username}' already exists")
        role = self.role_repository.get_role_by_name(user.role)
        if not role:
            raise HTTPException(
                status_code=400, detail=f"Role '{user.role}' does not exist"
            )

        is_active = False if role.name == "Author" else True
        hashed_password = self.hash_password(user.password)
        new_user = User(
            email=user.email,
            username=user.username,
            password=hashed_password,
            role_id=role.id,
            is_active=is_active,
        )
        return self.user_repository.create_user(new_user)
