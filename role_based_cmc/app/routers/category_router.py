from typing import List

from fastapi import APIRouter
from app.schemas.category_schema import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryWithArticles,
)
from uuid import UUID

router = APIRouter()


@router.post(
    "/",
    summary="Create Category",
    description="Allows Admins and Editors to create a new category.",
    response_model=CategoryResponse,
)
def create_category(category: CategoryCreate):
    pass


@router.put(
    "/{category_id}",
    summary="Update Category",
    description="Allows Admins and Editors to update an existing category.",
    response_model=CategoryResponse,
)
def update_category(category_id: UUID, category: CategoryUpdate):
    pass


@router.delete(
    "/{category_id}",
    summary="Delete Category",
    description="Allows Admins and Editors to delete a category.",
    response_model=CategoryResponse,
)
def delete_category(category_id: UUID):
    pass


@router.get(
    "/categories",
    summary="Get All Categories",
    description="Fetches a list of all categories.",
    response_model=List[CategoryResponse],
)
def get_all_categories():
    pass


@router.get(
    "/{category_id}",
    summary="Get Category",
    description="Fetches a specific category.",
    response_model=CategoryResponse,
)
def get_category(category_id: UUID):
    pass


@router.get(
    "/{category_id}/articles",
    summary="Get Category with Articles",
    description="Fetches a specific category along with "
                "its associated articles.",
    response_model=CategoryWithArticles,
)
def get_category_with_articles(category_id: UUID):
    pass
