from docutils.nodes import title
from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List

from fastapi.params import Depends
from sqlalchemy.sql.functions import current_user
from starlette.requests import Request
from unicodedata import category

from app.entities.schemas.article_schema import AuthorArticleResponse, ArticleResponse
from app.services.article_service import ArticleService
from app.services.user_service import UserService
from app.utils.auth_utils import get_current_author
from app.utils.fastapi.dependencies import require_role

router=APIRouter()


@router.get(
    "/articles/",
    response_model=List[AuthorArticleResponse],
    summary="Get all articles (Author)",
    description="Get all articles specific to the author",
    dependencies=[Depends(require_role(["Author"]))],
)
async def get_author_articles(
    author=Depends(get_current_author)
):
    return [
        AuthorArticleResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            tags=[tag.name for tag in article.tags],
            category=article.category.name,
            status=article.status,
            created_at=article.created_at,
            updated_at=article.updated_at,
        )
        for article in author.articles
    ]

@router.put(
     "/articles/{article_id}/submit",
      summary="Submit Article for Review",
      response_model=ArticleResponse,
      description="Allows authors to submit their own articles for review by changing the status to 'In Review'.",
      dependencies=[Depends(require_role(["Author"]))],
    )
async def submit_article_for_review(
            article_id: UUID,
            author=Depends(get_current_author),
            article_service: ArticleService = Depends(),
    ):
        print("Author",author)
        article = next((article for article in author.articles if article.id == article_id), None)
        print("Article",article.title)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found or not owned by the author")

        try:
            updated_article = article_service.submit_article(article, "In Review")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

        return ArticleResponse(
            id=updated_article.id,
            title=updated_article.title,
            content=updated_article.content,
            tags=[tag.name for tag in updated_article.tags],
            category=updated_article.category.name,
            status=updated_article.status,
            created_at=updated_article.created_at,
            updated_at=updated_article.updated_at,
            author=updated_article.author.username,
        )