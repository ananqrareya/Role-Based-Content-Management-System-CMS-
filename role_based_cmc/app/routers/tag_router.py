from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.entities.schemas.tag_schema import TagResponse, TagCreate

from uuid import UUID

from app.repositories.tags_repository import TagsRepository
from app.services.tags_service import TagsService
from app.entities.schemas.tag_schema import Tag
router = APIRouter()


@router.post(
    "/",
    summary="Create Tag",
    description="Allows Admins and Editors to create a new tag.",
    response_model=TagResponse,
)
def create_tag(tag: TagCreate, db:Session=Depends(get_db)):
    try:
        tag_repository=TagsRepository(db)
        tag_service=TagsService(tag_repository)
        new_tag=tag_service.create_tag(tag)
        message="Tag created successfully."
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
)
def get_all_tags(db:Session=Depends(get_db)):
    try:
        tag_repository=TagsRepository(db)
        tag_service=TagsService(tag_repository)
        tags=tag_service.get_all_tags()
        return[
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
)
def delete_tag(tag_id: UUID,db:Session=Depends(get_db)):
    try:
        tag_repository=TagsRepository(db)
        tag_service=TagsService(tag_repository)
        tag_delete=tag_service.delete_tag(tag_id)
        message="Tag deleted successfully."
        return TagResponse(
            tag=Tag(
                id=tag_delete.id,
                name=tag_delete.name,
            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

