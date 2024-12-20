from typing import List
from uuid import UUID

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.entities.models import Categories
from app.entities.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.repositories.categories_repository import CategoriesRepository


class CategoriesService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.categories_repository = CategoriesRepository(db)

    def create_category(self, category: CategoryCreate):
        if self.categories_repository.check_category_exists(category.name):
            raise ValueError(f"Category with name "
                             f"{category.name} already exists")

        category_db = Categories(
            name=category.name,
            description=category.description,
        )
        return self.categories_repository.add_category(category_db)

    def update_category(self, category_id: UUID,
                        category_update: CategoryUpdate):
        category_old = (self.categories_repository
                        .get_category_by_id(category_id))
        if category_old is None:
            raise HTTPException(status_code=404, detail="Category not found")
        category_db = self.categories_repository.update_category(
            category_old, category_update
        )
        return category_db

    def delete_category(self, category_id: UUID):
        category_db = (self.categories_repository
                       .get_category_by_id(category_id))
        if category_db is None:
            raise HTTPException(status_code=404, detail="Category not found")
        self.categories_repository.delete_category(category_db)
        return category_db

    def get_all_categories(self) -> List[Categories]:
        return self.categories_repository.get_all_categories()

    def get_category_by_id(self, category_id: UUID) -> Categories:
        category_db = (self.categories_repository
                       .get_category_by_id(category_id))
        if category_db is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return category_db
