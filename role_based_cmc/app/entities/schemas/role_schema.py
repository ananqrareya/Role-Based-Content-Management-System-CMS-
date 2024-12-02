from typing import Optional

from pydantic import BaseModel, Field
from uuid import UUID



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

    class Config:
        json_schema_extra = {
            "example": {
                "role": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Reader",
                    "description": "Can only view published articles",
                }
            }
        }
