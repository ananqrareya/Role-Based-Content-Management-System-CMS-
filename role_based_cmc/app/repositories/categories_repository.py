from sqlalchemy.orm import Session

from app.entities.models import Categories
from uuid import UUID

from app.entities.schemas.category_schema import CategoryUpdate


class CategoriesRepository:
    def __init__(self, session: Session):
        self.session = session

    def check_category_exists(self, category_name: str) -> bool:
        return (self.session.query(Categories)
                .filter(Categories.name == category_name).first())

    def get_category_by_id(self, category_id: UUID) -> Categories:
        return self.session.query(Categories).get(category_id)

    def add_category(self, category:Categories)->Categories:
        try:
            self.session.add(category)
            self.session.commit()
            return category
        except Exception as e:
            self.session.rollback()
            raise e

    def update_category(self,category_db:Categories , category_update:CategoryUpdate)->Categories:
        update_data = category_update.dict(exclude_unset=True)  # Exclude fields not provided
        for key, value in update_data.items():
            if value is not None:
                setattr(category_db, key, value)
        self.session.commit()
        self.session.refresh(category_db)
        return category_db

    def delete_category(self,category:Categories)->Categories:
        try:
            self.session.delete(category)
            self.session.commit()
            return category
        except Exception as e:
            self.session.rollback()
            raise e
    def get_all_categories(self ):
        try:
            return self.session.query(Categories).all()
        except Exception as e:
            self.session.rollback()
            raise e