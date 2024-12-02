from sqlalchemy.orm import Session
from app.entities.models.Roles import Roles


class RoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_role_by_name(self, role_name: str) -> Roles:
        return (self.session.query(Roles)
                .filter(Roles.name == role_name).first())

    def create_role(self, role: Roles) -> Roles:

        try:
            self.session.add(role)
            self.session.commit()
            self.session.refresh(role)
            return role
        except Exception as e:
            self.session.rollback()
            print(f"Error while creating role: {e}")
            return None

    def get_all_roles(self) -> list[Roles]:
        return self.session.query(Roles).all()

    def delete_role(self, role_name: str):
        raise ValueError("Deleting roles is not allowed.")
