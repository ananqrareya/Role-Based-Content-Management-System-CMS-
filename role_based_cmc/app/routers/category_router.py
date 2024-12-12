from typing import List

from conda_env.cli.main_list import description
from fastapi import APIRouter,HTTPException
from fastapi.params import Depends
from requests import delete
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.entities.models import Categories
from app.entities.schemas.category_schema import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryWithArticles, Category, CategoryUpdateResponse,
)
from uuid import UUID

from app.repositories.categories_repository import CategoriesRepository
from app.services.categories_service import CategoriesService

router = APIRouter()


@router.post(
    "/",
    summary="Create Category",
    description="Allows Admins and Editors to create a new category.",
    response_model=CategoryResponse,
)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    category_repository = CategoriesRepository(db)
    category_service=CategoriesService(category_repository)
    try:
        new_category = category_service.create_category(category)
        message="The category was successfully created."
        return CategoryResponse(
            category=Category(
                id=new_category.id,
                name=new_category.name,
                description=new_category.description,
            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))





@router.put(
    "/{category_id}",
    summary="Update Category",
    description="Allows Admins and Editors to update an existing category.",
    response_model=CategoryUpdateResponse,
)
def update_category(category_id: UUID, category: CategoryUpdate , db: Session = Depends(get_db)):
    try:
        category_repository = CategoriesRepository(db)
        category_service = CategoriesService(category_repository)
        updated_category = category_service.update_category(category_id, category)
        message="The category was successfully updated."
        return CategoryUpdateResponse(
            category=CategoryUpdate(
                name=updated_category.name,
                description=updated_category.description,

            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{category_id}",
    summary="Delete Category",
    description="Allows Admins and Editors to delete a category.",
    response_model=CategoryResponse,
)
def delete_category(category_id: UUID,db: Session = Depends(get_db)):
    try:
        category_repository = CategoriesRepository(db)
        category_service = CategoriesService(category_repository)
        category_delete=category_service.delete_category(category_id)
        message="The category was successfully deleted."
        return CategoryResponse(
            category=Category(
                id=category_delete.id,
                name=category_delete.name,
                description=category_delete.description,
            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get(
    "/categories",
    summary="Get All Categories",
    description="Fetches a list of all categories.",
    response_model=List[Category],
)
def get_all_categories(db:Session=Depends(get_db)):
    try:
        category_repository = CategoriesRepository(db)
        category_service = CategoriesService(category_repository)
        categories=category_service.get_all_categories()
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description
            )
            for category in categories
        ]
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get(
    "/{category_id}",
    summary="Get Category",
    description="Fetches a specific category.",
    response_model=CategoryResponse,
)
def get_category(category_id: UUID,db:Session=Depends(get_db)):
    try:
        category_repository = CategoriesRepository(db)
        category_service = CategoriesService(category_repository)
        category=category_service.get_category_by_id(category_id)
        return CategoryResponse(
            category=Category(
                id=category.id,
                name=category.name,
                description=category.description,
            ),
            message="Successfully fetched category.",
        )
    except ValueError as e:
        raise HTTPException(status_code=500,detail=str(e))



@router.get(
    "/{category_id}/articles",
    summary="Get Category with Articles",
    description="Fetches a specific category along with "
                "its associated articles.",
    response_model=CategoryWithArticles,
)
def get_category_with_articles(category_id: UUID):
    pass
