from pydantic import BaseModel, Field
from uuid import UUID


class TagCreate(BaseModel):
    name: str = Field(..., max_length=55, description="Name of the tag")

    class Config:
        json_schema_extra = {"example": {"name": "Technology"}}


class Tag(BaseModel):
    id: UUID
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Technology",
            }
        }
class TagResponse(BaseModel):
    tag:Tag
    message:str
    class Config:
        json_schema_extra = {
            "example": {
                "Tag":{
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Technology",
                },
                "message": "Tag created"
            }
        }