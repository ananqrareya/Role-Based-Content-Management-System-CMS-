from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, validator
from uuid import UUID


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.upper() for char in v):
            raise ValueError("Password must"
                             " contain at least one uppercase letter")
        if not any(char.lower() for char in v):
            raise ValueError("Password must "
                             "contain at least one lowercase letter")
        if not any(char in "!@#%$*" for char in v):
            raise ValueError("Password must "
                             "contain at least one special character")
        return v


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
    role: str = Field(..., description="User's role in the system")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "ananqrareya",
                "email": "ananqrareya@gmail.com",
                "is_active": True,
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-11-18T15:00:00",
                "role": "Admin",
            }
        }


class RegisterRequest(UserSchema):
    role: str = Field(..., description="User's role in the system")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "username": "ananqrareya",
                    "email": "ananqrareya@gmail.com",
                    "password": "SecureP@ssw0rd123",
                    "role": "Admin",
                }
            ]
        }


class RegisterResponse(BaseModel):

    user: UserResponse

    class Config:
        json_schema_extra = {
            "example": {
                "message": "User registered successfully.",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "ananqrareya",
                    "email": "ananqrareya@gmail.com",
                    "is_active": True,
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-11-18T15:00:00",
                    "role": "Admin",
                },
            }
        }


class UserUpdateRequest(BaseModel):
    role: str

    class Config:
        json_schema_extra = {"example": {"role": "Editor"}}


class UserUpdateResponse(BaseModel):
    message: str
    user: UserResponse

    class Config:
        json_schema_extra = {
            "example": {
                "message": "User Update Role successfully.",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "ananqrareya",
                    "email": "ananqrareya@gmail.com",
                    "is_active": True,
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-11-18T15:00:00",
                    "role": "Admin",
                },
            }
        }
