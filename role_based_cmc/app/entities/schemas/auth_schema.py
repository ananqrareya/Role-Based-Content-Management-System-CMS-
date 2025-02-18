from pydantic import BaseModel, Field, ConfigDict


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "ananqrareya",
                "password": "SecureP@ssw0rd123",
            }
        }
    )

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    )