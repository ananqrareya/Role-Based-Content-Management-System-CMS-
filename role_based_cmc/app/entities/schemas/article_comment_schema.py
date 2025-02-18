from typing import List

from black import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class CommentCreate(BaseModel):
    text: str

    model_config = ConfigDict(json_schema_extra={"example": {"text": "This is a helpful article!"}})

class CommentResponse(BaseModel):
    id: UUID
    content: str
    article: str
    user: str
    created_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "content": "This is a helpful article!",
                "article_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2024-11-18T15:00:00",
            }
        }
    )

class CommentUpdate(BaseModel):
    text: str

    model_config = ConfigDict(json_schema_extra={"example": {"text": "This is the updated comment content."}})



class Comment(BaseModel):
    id: UUID
    content: str
    user: str
    created_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "content": "This is a helpful article!",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2024-11-18T15:00:00",
            }
        }
    )


class CommentInArticle(BaseModel):
    article_title: str
    comments: List[Comment]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "article_title": "Understanding Python Decorators",
                "comments": [
                    {
                        "id": "660e8400-e29b-41d4-a716-446655440001",
                        "content": "Great explanation of decorators!",
                        "user_id": "123e4567-e89b-12d3-a456-426614174001",
                        "created_at": "2024-11-19T10:00:00",
                    },
                    {
                        "id": "660e8400-e29b-41d4-a716-446655440002",
                        "content": "This cleared up a lot of confusion for me.",
                        "user_id": "123e4567-e89b-12d3-a456-426614174002",
                        "created_at": "2024-11-19T12:00:00",
                    },
                ],
            }
        }
    )