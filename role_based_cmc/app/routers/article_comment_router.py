from fastapi import APIRouter
from uuid import UUID
from typing import List
from app.entities.schemas.article_comment_schema import (
    CommentResponse,
    CommentCreate,
    CommentUpdate,
)

router = APIRouter()


@router.post(
    "/{article_id}/comment",
    summary="Add Comment to an Article",
    description="Allows any authenticated user"
                " to add a comment to a specific article.",
    response_model=CommentResponse,
)
def add_comment(article_id: UUID, comment: CommentCreate):
    pass


@router.get(
    "/{article_id}/comment",
    summary="Get Comments for an Article",
    description="Fetches all comments for a specific article.",
    response_model=List[CommentResponse],
)
def get_comments(article_id: UUID):
    pass


@router.put(
    "/comment/{comment_id}",
    summary="Update Comment",
    description="Allows a user to update their own comment"
                " or allows Admins/Editors to update any comment.",
    response_model=CommentResponse,
)
def update_comment(comment_id: UUID, comment: CommentUpdate):
    pass


@router.delete(
    "/comments/{article_id}",
    summary="Delete Comment",
    description="Allows Admins and Editors to delete any comment.",
    response_model=CommentResponse,
)
def delete_comment(article_id: UUID):
    pass
