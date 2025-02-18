from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class TagCreate(BaseModel):
    name: str = Field(..., max_length=55, description="Name of the tag")

    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "Technology"}}
    )

class Tag(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Technology",
            }
        }
    )



class TagResponse(BaseModel):
    tag: Tag
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "tag": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Technology",
                },
                "message": "Tag created",
            }
        }
    )