from fastapi import APIRouter
from typing import List, Optional

from app.schemas.article_schema import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleStatusUpdate,
)
from app.enums.article_status import ArticleStatus
from uuid import UUID

router = APIRouter()


@router.post(
    "/",
    response_model=ArticleResponse,
    summary="Create an Article (Author) ",
    description="""
    Allows authors to create a new article. 
    The created article will have a default status of 'Draft'.
    Only users with the role 'Author' are allowed to access this endpoint.
    """
)
def create_article(article: ArticleCreate):
    pass


@router.get(
    "/",
    response_model=List[ArticleResponse],
    summary="Get All Articles (Admin,Editor)",
    description="""
    Fetches all articles with optional filters for status.
    Only Admins and Editors can access this endpoint. 
    Supports query parameters for filtering articles by:
    - `status`: Status of the article (e.g., 'Draft', 'Published').
    """
)
def get_published_articles(status: Optional[ArticleStatus] = None):
    pass


@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Get a single Article (Admin,Editor) ",
    description="""
    Fetches the details of a single article by its ID.
    Only Admins and Editors can access this endpoint.
    """,
)
def get_article(article_id: UUID):
    pass


@router.put(
    "{article_id}",
    response_model=ArticleResponse,
    summary="Update article  By:(Author,Admin,Editor)",
    description="""
    Allows updating an article by its ID. 
    - Authors can update only their own articles.
    - Admins and Editors can update any article.
    """,
)
def update_article(article_id: UUID, article_update: ArticleUpdate):
    pass


@router.delete(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Delete an Article (Admin,Editor)",
    description="""
    Deletes an article by its ID. Only Admins and Editors can perform this action.
    """,
)
def delete_article(article_id: UUID):
    pass


@router.patch(
    "/{article_id}/status",
    response_model=ArticleResponse,
    summary="Update article status  By only:(Admin,Editor)",
    description="""
    Updates the status of an article 
    (e.g., 'Draft', 'In Review', 'Published', 'Rejected').
    Only Admins and Editors are allowed to perform this action.
    """,
)
def update_article_status(article_id: UUID, status_update: ArticleStatusUpdate):
    pass


@router.put(
    "/{article_id}/submit",
    summary="Submit Article for Review",
    response_model=ArticleResponse,
    description="Allows authors to submit their own articles for review by changing the status to 'In Review'.",
)
def submit_article_for_review(article_id: UUID):
    pass


@router.put(
    "/{article_id}/publish",
    summary="Publish Article",
    response_model=ArticleResponse,
    description="Allows editors and admins to change the status of an article to 'Published'.",
)
def publish_article(
    article_id: UUID,
):
    pass


@router.get(
    "/published",
    summary="Get All Published Articles (Readers)",
    response_model=List[ArticleResponse],
    description="""
    Fetches all published articles.
    This endpoint is primarily for readers or public access.
    """,
)
def get_published_articles():
    pass


@router.get(
    "/search",
    response_model=List[ArticleResponse],
    summary="Search Articles (Readers)",
    description="""
    Search for articles based on:
    - `categories`: Filter by category IDs.
    - `tags`: Filter articles containing specific tags.
    - `keyword`: Search for articles containing the keyword in their title 
    or content.
    Only published articles are returned.
    The author can view any published article.
    """
)
def search_articles(
    categories: Optional[List[UUID]] = None,
    tags: Optional[List[str]] = None,
    keyword: Optional[str] = None,
):
    pass


@router.get(
    "/filter",
    response_model=List[ArticleResponse],
    summary="Filter Articles (Readers)",
    description="""
    Filter articles based on:
    - `status`: The publication status of the article (e.g., Published).
    - `author_id`: Filter by the author's unique ID.
    - `date`: Filter articles created on a specific date.
    Only published articles are returned for readers.
    The author can view any published article.
    """,
)
def filter_articles(
    status: Optional[ArticleStatus] = None,
    author_id: Optional[UUID] = None,
    date: Optional[str] = None,
):
    pass
