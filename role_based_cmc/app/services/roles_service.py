from app.models import Roles
from app.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def create_role_if_not_exists(self, role_name: str):
        existing_role = self.role_repository.get_role_by_name(role_name)
        if not existing_role:
            new_role = Roles(name=role_name, description=f"{role_name} role")
            return self.role_repository.create_role(new_role)
        return existing_role
