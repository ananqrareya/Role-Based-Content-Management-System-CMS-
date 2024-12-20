from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List

from fastapi.params import Depends
from starlette.requests import Request

from app.entities.models import Comments
from app.entities.schemas.article_comment_schema import (
    CommentResponse,
    CommentCreate,
    CommentUpdate, CommentInArticle, Comment,
)
from app.services.article_comment_service import ArticleCommentService
from app.utils.fastapi.dependencies import require_role

router = APIRouter()


@router.post(
    "/{article_id}/comment",
    summary="Add Comment to an Article",
    description="Allows any authenticated user"
                " to add a comment to a specific article.",
    response_model=CommentResponse,
)
def add_comment(article_id: UUID, comment: CommentCreate,
                request:Request,
                article_comment_service:ArticleCommentService=Depends()):
    try:
        current_user=request.state.user
        comment_db=article_comment_service.new_comment(article_id, comment.text,user_id=current_user.get("user_id"))
        return CommentResponse(
            id=comment_db.id,
            content=comment_db.content,
            user=comment_db.user.username,
            article=comment_db.article.title,
            created_at=comment_db.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{article_id}/comment",
    summary="Get Comments for an Article",
    description="Fetches all comments for a specific article.",
    response_model=CommentInArticle,
)
def get_comments(article_id: UUID,article_comment_service:ArticleCommentService=Depends()):
    try:
        article_with_comments = article_comment_service.get_article_with_comment(article_id)
        return CommentInArticle(
            article_title=article_with_comments.title,
            comments=[
                Comment(
                    id=comment.id,
                    content=comment.content,
                    user=comment.user.username,
                    created_at=comment.created_at,
                )
                for comment in article_with_comments.comments
            ],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.put(
    "/comment/{comment_id}",
    summary="Update Comment",
    description="Allows a user to update their own comment"
                " or allows Admins/Editors to update any comment.",
    response_model=CommentResponse,
    dependencies=[Depends(require_role(["Admin","Editor"]))],
)
def update_comment(comment_id: UUID, comment: CommentUpdate,article_comment_service:ArticleCommentService=Depends()):
    try:
        update_comment=article_comment_service.update_comment(comment_id,comment.text)
        return CommentResponse(
            id=update_comment.id,
            content=update_comment.content,
            user=update_comment.user.username,
            article=update_comment.article.title,
            created_at=update_comment.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/comment/{comment_id}",
    summary="Delete Comment",
    description="Allows Admins and Editors to delete any comment.",
    response_model=CommentResponse,
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
def delete_comment(
    comment_id: UUID,
    article_comment_service: ArticleCommentService = Depends()
):
    try:
        deleted_comment = article_comment_service.delete_comment(comment_id)
        return CommentResponse(
            id=deleted_comment.id,
            content=deleted_comment.content,
            user=deleted_comment.user.username,
            article=deleted_comment.article.title,
            created_at=deleted_comment.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

