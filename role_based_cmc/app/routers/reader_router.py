from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.entities.enums.article_status import ArticleStatus
from app.entities.schemas.article_schema import ArticleResponse
from app.services.article_service import ArticleService
from app.utils.fastapi.dependencies import require_role
from typing import List, Optional
from uuid import UUID
router=APIRouter()

@router.get(
    "/article/all-published",
    summary="Get All Published Articles (Readers)",
    response_model=List[ArticleResponse],
    description="""
    Fetches all published articles.
    This endpoint is primarily for readers or public access.
    """,
    dependencies=[Depends(require_role(["Reader"]))],
)
def get_published_articles(article_service:ArticleService=Depends()):
    try:
        published_articles=article_service.get_articles_by_status(ArticleStatus.PUBLISHED)
        if not published_articles:
            raise HTTPException(status_code=404, detail="No published articles found.")
        return [
            ArticleResponse(
                id=article.id,
                title=article.title,
                content=article.content,
                tags=[tag.name for tag in article.tags],
                category=article.category.name,
                status=article.status,
                author=article.author.username,
                created_at=article.created_at,
                updated_at=article.updated_at,
            )
            for article in published_articles
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error processing articles: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get(
    "/article/search",
    response_model=List[ArticleResponse],
    summary="Search Articles (Readers)",
    description="""
    Search for articles based on:
    - `categories`: Filter by category IDs.
    - `tags`: Filter articles containing specific tags.
    - `keyword`: Search for articles containing the keyword in their title 
    or content.
    Only published articles are returned.
    """,
    dependencies=[Depends(require_role(["Reader"]))],
)
async def search_articles(
    categories: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    keyword: Optional[str] = None,
    article_service:ArticleService=Depends()
):
    try:
        articles=article_service.search_articles(categories=categories, tags=tags, keyword=keyword)
        return articles
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error processing articles: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.get(
    "/article/filter",
    response_model=List[ArticleResponse],
    summary="Filter Articles (Readers)",
    description="""
    Filter articles based on:
    - `status`: The publication status of the article (e.g., Published).
    - `author_id`: Filter by the author's unique ID.
    - `date`: Filter articles created on a specific date.
    Only published articles are returned for readers.
    """,
    dependencies=[Depends(require_role(["Reader"]))],
)
def filter_articles(
    author: Optional[str] = None,
    date: Optional[str] = None,
    article_service:ArticleService=Depends()
):
    try:
        article=article_service.filter_article(author=author, date=date)
        return article
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error processing articles: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
