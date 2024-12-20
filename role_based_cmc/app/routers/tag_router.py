from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.entities.schemas.tag_schema import (TagResponse,
                                             TagCreate)
from uuid import UUID
from app.services.tags_service import TagsService
from app.entities.schemas.tag_schema import Tag
from app.utils.fastapi.dependencies import require_role

router = APIRouter()


@router.post(
    "/",
    summary="Create Tag",
    description="Allows Admins and Editors to create a new tag.",
    response_model=TagResponse,
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def create_tag(tag: TagCreate, tag_service: TagsService = Depends()):
    try:
        new_tag = tag_service.create_tag(tag)
        message = "Tag created successfully."
        return TagResponse(
            tag=Tag(
                id=new_tag.id,
                name=new_tag.name,
            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    summary="Get All Tags",
    description="Fetches a list of all tags.",
    response_model=List[Tag],
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def get_all_tags(tag_service: TagsService = Depends()):
    try:
        tags = tag_service.get_all_tags()
        return [
            Tag(
                id=tag.id,
                name=tag.name,
            )
            for tag in tags
        ]
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{tag_id}",
    summary="Delete Tag",
    description="Allows Admins and Editors to delete a tag.",
    response_model=TagResponse,
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def delete_tag(tag_id: UUID, tag_service: TagsService = Depends()):
    try:
        tag_delete = tag_service.delete_tag(tag_id)
        message = "Tag deleted successfully."
        return TagResponse(
            tag=Tag(
                id=tag_delete.id,
                name=tag_delete.name,
            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500,
                            detail="An unexpected error occurred")
