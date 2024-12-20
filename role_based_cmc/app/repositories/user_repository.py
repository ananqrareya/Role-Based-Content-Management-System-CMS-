from sqlalchemy.orm import Session

from app.entities.models import Roles
from app.entities.models.User import User
from uuid import UUID


class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_all_user(self):
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: UUID):
        print("repo", user_id)
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_inactive(self):
        return (self.db.query(User)
                .filter(User.is_active == False).all())

    def create_user(self, user: User):
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise e

    def update_role_user(self, user: User, role: Roles):
        try:
            if user.is_active == False:
                user.is_active = True

            user.role_id = role.id
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error updating user role: {str(e)}")

    def active_user(self, user: User):
        try:
            user.is_active = True
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error updating user role: {str(e)}")

    def delete_user(self, user: User):
        try:
            self.db.delete(user)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error deleting user role: {str(e)}")
