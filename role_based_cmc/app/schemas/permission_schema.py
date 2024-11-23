from typing import Optional

from black import datetime
from pydantic import BaseModel
from uuid import UUID


class PermissionBase(BaseModel):
    permission_id: UUID

    class Config:
        json_schema_extra = {
            "example": {
                "permission_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class Permission(PermissionBase):
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "permissions": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "manage_users",
                        "description": "Ability to manage "
                                       "user accounts and roles",
                    },
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "name": "view_articles",
                        "description": "Ability to view published articles",
                    },
                ]
            }
        }


class PermissionResponse(BaseModel):
    id: UUID
    name: str
    description: str
