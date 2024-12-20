from uuid import UUID

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.entities.models import Roles
from app.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.role_repository = RoleRepository(db)

    def create_role_if_not_exists(self, role_name: str):
        existing_role = self.role_repository.get_role_by_name(role_name)
        if not existing_role:
            new_role = Roles(name=role_name, description=f"{role_name} role")
            return self.role_repository.create_role(new_role)
        return existing_role

    def get_all_role(self):
        return self.role_repository.get_all_roles()

    def get_role_with_users(self, role_id: UUID):
        role_db = self.role_repository.get_role_by_id(role_id)
        if not role_db:
            raise HTTPException(status_code=409, detail="Role not found")
        return self.role_repository.get_role_with_users(role_db)
