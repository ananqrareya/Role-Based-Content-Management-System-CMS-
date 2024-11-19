from typing import Optional

from pydantic import BaseModel, Field
from uuid import UUID

from app.schemas.permission_schema import PermissionResponse


class RoleSchema(BaseModel):
    id: UUID = Field(default=None,
                     description="Unique identifier for the role")
    name: str = Field(
        ..., max_length=50, description="Name of the role, must be unique"
    )
    description: str = Field(..., description="Description of the role")


class RoleCreateRequest(BaseModel):
    name: str = Field(
        ..., max_length=50, description="Name of the role, must be unique"
    )
    description: str = Field(..., description="Description of the role")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Author",
                "description": "Author of the role",
            }
        }


class RoleUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None, max_length=50, description="Name of the role, must be unique"
    )
    description: Optional[str] = Field(
        None, max_length=50, description="Description of the role"
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                 "name": "Admin",
                 "description": "Administrator role"
                 }
            ]
        }


class RoleResponse(BaseModel):
    role: RoleSchema
    permissions: list[PermissionResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "role": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Reader",
                    "description": "Can only view published articles",
                    "permissions": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "name": "manage_users",
                            "description": "Ability to"
                                           " manage user accounts and roles",
                        },
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174001",
                            "name": "view_articles",
                            "description": "Ability to "
                                           "view published articles",
                        },
                    ],
                }
            }
        }
