from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class CommentCreate(BaseModel):
    text: str

    class Config:
        json_schema_extra = {"example": {"text": "This is a helpful article!"}}


class CommentResponse(BaseModel):
    id: UUID
    content: str
    article_id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440000",
                "content": "This is a helpful article!",
                "article_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2024-11-18T15:00:00",
            }
        }


class CommentUpdate(BaseModel):
    text: str

    class Config:
        json_schema_extra = {
            "example": {"text": "This is the updated comment content."}
        }
