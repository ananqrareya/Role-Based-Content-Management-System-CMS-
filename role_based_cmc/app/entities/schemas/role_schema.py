

from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class RoleSchema(BaseModel):
    id: UUID = Field(default=None,
                     description="Unique identifier for the role")
    name: str = Field(
        ..., max_length=50, description="Name of the role, must be unique"
    )
    description: str = Field(..., description="Description of the role")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Reader",
                "description": "Can only view published articles",
            }
        }


class UserSchema(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool


class RoleWithUsersSchema(BaseModel):
    role: RoleSchema
    users: list[UserSchema]
