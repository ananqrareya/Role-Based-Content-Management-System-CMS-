import uuid
from typing import List
from uuid import UUID

from unicodedata import category

from app.entities.models import Categories
from app.entities.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.repositories.categories_repository import CategoriesRepository


class CategoriesService:
    def __init__(self , categories_repository:CategoriesRepository):
        self.categories_repository = categories_repository

    def create_category(self , category:CategoryCreate):
        if self.categories_repository.check_category_exists(category.name):
            raise ValueError(f'Category with name {category.name} already exists')

        category_db=Categories(
            name=category.name,
            description=category.description,
        )
        return self.categories_repository.add_category(category_db)


    def update_category(self, category_id:UUID , category_update:CategoryUpdate):
        category_old=self.categories_repository.get_category_by_id(category_id)
        if category_old is None:
            raise ValueError(f'Category with id {category_id} does not exist')
        category_db=self.categories_repository.update_category(category_old,category_update)
        return category_db

    def delete_category(self, category_id:UUID):
        category_db=self.categories_repository.get_category_by_id(category_id)
        if category_db is None:
            raise ValueError(f'Category with id {category_id} does not exist')
        self.categories_repository.delete_category(category_db)
        return category_db
    def get_all_categories(self)->List[Categories]:
        return self.categories_repository.get_all_categories()

    def get_category_by_id(self, category_id:UUID)->Categories:
        category_db=self.categories_repository.get_category_by_id(category_id)
        if category_db is None:
            raise ValueError(f'Category with id {category_id} does not exist')
        return category_db
