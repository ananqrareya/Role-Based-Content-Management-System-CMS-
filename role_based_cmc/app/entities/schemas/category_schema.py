from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


from app.entities.schemas.article_schema import ArticleBrief


class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=55,
                      description="Unique name for the category")
    description: str = Field(None, description="Description of the category")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Programming",
                "description": "Articles about programming languages and techniques.",
            }
        }
    )


class Category(BaseModel):
    id: UUID
    name: str
    description: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Programming",
                "description": "Articles about programming languages and techniques.",
            }
        }
    )

class CategoryResponse(BaseModel):
    category: Category
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "The category was successfully created.",
                "category": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Programming",
                    "description": "Articles about programming languages and techniques.",
                },
            }
        }
    )


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(
        None, max_length=55, description="Name of the category, must be unique"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Description of the category",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Programming Api",
                    "description": "Articles about programming"
                                   " languages and techniques.",
                }
            ]
        }
    )

class CategoryUpdateResponse(BaseModel):
    category: CategoryUpdate
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "The category was successfully updated.",
                "category": {
                    "name": "Programming",
                    "description": "Articles about programming"
                                   " languages and techniques.",
                },
            }
        }
    )


class CategoryWithArticles(BaseModel):
    id: UUID
    name: str
    description: str
    articles: list[ArticleBrief]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Programming",
                "description": "Articles about programming languages and techniques.",
                "articles": [
                    {
                        "id": "660e8400-e29b-41d4-a716-446655440000",
                        "title": "Introduction to FastAPI",
                        "content": "Learn the basics of FastAPI...",
                    },
                    {
                        "id": "770e8400-e29b-41d4-a716-446655440001",
                        "title": "Python Tips and Tricks",
                        "content": "Advanced Python tips for developers...",
                    },
                ],
            }
        }
    )