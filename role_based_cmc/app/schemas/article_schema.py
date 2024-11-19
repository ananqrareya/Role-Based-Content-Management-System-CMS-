from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Optional

from app.enums.article_status import ArticleStatus
from uuid import UUID


class ArticleSchema(BaseModel):
    title: str = Field(..., max_length=55, description="Title of the article")
    content: str
    tag: List[str]
    category: str

    class Config:
        class Config:
            json_schema_extra = {
                "examples": [
                    {
                        "title": "FastAPI Guide",
                        "content": "Comprehensive guide on FastAPI.",
                        "tags": ["Python", "FastAPI"],
                        "category": "Programming",
                    }
                ]
            }


class ArticleBrief(BaseModel):
    id: UUID
    title: str
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "title": "Introduction to FastAPI",
                "content": "Learn the basics of FastAPI...",
            }
        }


class ArticleCreate(ArticleSchema):
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "How to Use Pydantic",
                    "content": "Learn to validate data with Pydantic.",
                    "tags": ["Python", "Validation"],
                    "category": "programming",
                }
            ]
        }


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=55)
    content: Optional[str] = Field(None)
    tags: Optional[List[str]] = Field(None)
    category: Optional[str] = Field(None)
    status: Optional[ArticleStatus] = Field(None)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Updated FastAPI Guide",
                    "content": "Revised content for the guide.",
                    "tags": ["Python", "Guide"],
                    "category": "programming",
                    "status": "In Review",
                }
            ]
        }


class ArticleStatusUpdate(BaseModel):
    status: ArticleStatus

    class Config:
        json_schema_extra = {"example": {"status": "In Review"}}


class ArticleResponse(ArticleSchema):
    status: str
    author: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "FastAPI Guide",
                    "content": "Comprehensive guide on FastAPI.",
                    "tags": ["Python", "FastAPI"],
                    "category": "Programming",
                    "status": "In Review",
                    "author": "anan",
                    "created_at": "2024-11-18T12:34:56",
                    "updated_at": "2024-11-18T12:34:56",
                }
            ]
        }
