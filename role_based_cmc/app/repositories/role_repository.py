from psycopg2 import IntegrityError
from sqlalchemy.orm import Session, joinedload
from app.entities.models.Roles import Roles
from uuid import UUID


class RoleRepository:
    def __init__(self, session: Session):
        self.session = session



    def create_role(self, role: Roles) -> Roles:

        try:
            self.session.add(role)
            self.session.commit()
            self.session.refresh(role)
            return role
        except IntegrityError as e:
            self.session.rollback()
            raise e

    def get_all_roles(self) -> list[Roles]:
        return self.session.query(Roles).all()

    def get_role_with_users(self, role: Roles) -> Roles:
        return (self.session.query(Roles)
                .options(joinedload(Roles.users))
                .filter_by(id=role.id).first())

    def get_role_by_name(self, role_name: str) -> Roles:
        return (self.session.query(Roles)
                .filter(Roles.name == role_name).first())

    def get_role_by_id(self, role_id: UUID) -> Roles:
        return self.session.query(Roles).filter_by(id=role_id).first()
