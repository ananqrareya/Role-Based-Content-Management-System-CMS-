from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.entities.models.User import User
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.entities.schemas.user_schema import RegisterRequest
from app.utils.password_utils import hash_password
from app.utils.password_utils import verify_password
from uuid import UUID


class UserService:
    def __init__(
        self,
        db: Session = Depends(get_db),
    ):
        self.db = db
        self.user_repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    def create_admin_user(
        self, email: str, username: str, password: str, role_name: str
    ):

        if self.user_repository.get_user_by_email(email):
            raise ValueError(f"Email '{email}' already exists")

        role = self.role_repository.get_role_by_name(role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' does not exist")

        hashed_password = hash_password(password)
        admin_user = User(
            email=email, username=username,
            password=hashed_password, role_id=role.id
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
        hashed_password = hash_password(user.password)
        new_user = User(
            email=user.email,
            username=user.username,
            password=hashed_password,
            role_id=role.id,
            is_active=is_active,
        )
        return self.user_repository.create_user(new_user)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401,
                                detail="Invalid username or password")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        if not user.is_active:
            raise HTTPException(status_code=403,
                                detail="User account is inactive")

        return user

    def get_user_by_username(self, username: str):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def get_all_users(self):
        return self.user_repository.get_all_user()

    def get_user_by_id(self, id: UUID):
        user = self.user_repository.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def get_users_inactive(self):
        return self.user_repository.get_user_inactive()

    def update_role(self, user_id, role_name):
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        role = self.role_repository.get_role_by_name(role_name)
        if not role:
            raise HTTPException(
                status_code=404, detail=f"Role '{role_name}' does not exist"
            )
        return self.user_repository.update_role_user(user, role)

    def activate_user(self, user_id: UUID):
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_active == True:
            raise HTTPException(
                status_code=403, detail="User account already is active"
            )

        return self.user_repository.active_user(user)

    def delete_user(self, user: User):
        self.user_repository.delete_user(user)
