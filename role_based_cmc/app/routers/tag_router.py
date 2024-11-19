from typing import List

from fastapi import APIRouter

from app.schemas.tag_schema import TagResponse, TagCreate

from uuid import UUID

router = APIRouter()


@router.post(
    "/",
    summary="Create Tag",
    description="Allows Admins and Editors to create a new tag.",
    response_model=TagResponse,
)
def create_tag(tag: TagCreate):
    pass


@router.get(
    "/",
    summary="Get All Tags",
    description="Fetches a list of all tags.",
    response_model=List[TagResponse],
)
def get_all_tags():
    pass


@router.delete(
    "/{tag_id}",
    summary="Delete Tag",
    description="Allows Admins and Editors to delete a tag.",
    response_model=TagResponse,
)
def delete_tag(tag_id: UUID):
    pass
