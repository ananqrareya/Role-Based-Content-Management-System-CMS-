from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from app.entities.schemas.article_schema import ArticleBrief
from app.entities.schemas.category_schema import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryWithArticles,
    Category,
    CategoryUpdateResponse,
)
from uuid import UUID

from app.services.categories_service import CategoriesService
from app.utils.fastapi.dependencies import require_role

router = APIRouter()


@router.post(
    "/",
    summary="Create Category",
    description="Allows Admins and Editors to create a new category.",
    response_model=CategoryResponse,
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def create_category(
    category: CategoryCreate, category_service: CategoriesService = Depends()
):
    try:
        new_category = category_service.create_category(category)
        message = "The category was successfully created."
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
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def update_category(
    category_id: UUID,
    category: CategoryUpdate,
    category_service: CategoriesService = Depends(),
):
    try:
        updated_category = (category_service
                            .update_category(category_id, category))
        message = "The category was successfully updated."
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
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def delete_category(
    category_id: UUID, category_service: CategoriesService = Depends()
):
    try:
        category_delete = category_service.delete_category(category_id)
        message = "The category was successfully deleted."
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
    except Exception:
        raise HTTPException(status_code=500,
                            detail="An unexpected error occurred")


@router.get(
    "/categories",
    summary="Get All Categories",
    description="Fetches a list of all categories.",
    response_model=List[Category],
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def get_all_categories(category_service: CategoriesService = Depends()):
    try:
        categories = category_service.get_all_categories()
        return [
            Category(
                id=category.id, name=category.name,
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
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def get_category(
    category_id: UUID, category_service: CategoriesService = Depends()
):
    try:
        category = category_service.get_category_by_id(category_id)
        return CategoryResponse(
            category=Category(
                id=category.id,
                name=category.name,
                description=category.description,
            ),
            message="Successfully fetched category.",
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{category_id}/articles",
    summary="Get Category with Articles",
    description="Fetches a specific category along with "
                "its associated articles.",
    response_model=CategoryWithArticles,
    dependencies=[Depends(require_role(["Admin", "Editor", "Reader"]))],
)
async def get_category_with_articles(
    category_id: UUID, category_service: CategoriesService = Depends()
):
    try:
        category = category_service.get_category_by_id(category_id)
        articles = [
            ArticleBrief(id=article.id,
                         title=article.title,
                         content=article.content)
            for article in category.articles
        ]
        return CategoryWithArticles(
            id=category.id,
            name=category.name,
            description=category.description,
            articles=articles,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
