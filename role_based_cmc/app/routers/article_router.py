from docutils.nodes import title
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from fastapi.params import Depends
from starlette.requests import Request

from app.entities.enums import ArticleStatus
from app.entities.models import Articles
from app.entities.schemas.article_schema import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleStatusUpdate,
)

from uuid import UUID

from app.services.article_service import ArticleService
from app.utils.fastapi.dependencies import require_role

router = APIRouter()


@router.post(
    "/",
    response_model=ArticleResponse,
    summary="Create an Article (Author) ",
    description="""
    Allows authors to create a new article. 
    The created article will have a default status of 'Draft'.
    Only users with the role 'Author' are allowed to access this endpoint.
    """,
    dependencies=[Depends(require_role(["Admin", "Editor","Author"]))],
)
async def create_article(article: ArticleCreate,
                         request: Request,
                         article_service:ArticleService=Depends()
                         ):
    try:
         current_user = request.state.user
         print("the user:",current_user)
         if not current_user:
             raise HTTPException(status_code=401, detail="Not authenticated")
         try:
             category=article_service.check_category_id_with_article(article.category)
         except HTTPException as e:
             raise HTTPException(status_code=e.status_code, detail=e.detail)
         valid_tags = []
         for tag in article.tags:
             try:
                 valid_tag = article_service.check_tag_id_with_aritcle(tag)
                 valid_tags.append(valid_tag)
             except HTTPException as e:
                 raise HTTPException(status_code=e.status_code, detail=e.detail)

         new_article_data = {
              "title": article.title,
              "content": article.content,
              "author_id":current_user.get("user_id"),
              "category_id": category.id,
              "tags": valid_tags,
          }
         new_article=article_service.create_article(new_article_data)
         return ArticleResponse(
             id=new_article.id,
             title=new_article.title,
             content=new_article.content,
             tags=[tag.name for tag in new_article.tags],
             category=new_article.category.name,
             status=new_article.status,
             author=new_article.author.username,
             created_at=new_article.created_at,
             updated_at=new_article.updated_at,
         )


    except HTTPException as http_err:
        raise http_err
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/",
    response_model=List[ArticleResponse],
    summary="Get All Articles (Admin,Editor)",
    description="""
    Fetches all articles with optional filters for status.
    Only Admins and Editors can access this endpoint. 
    Supports query parameters for filtering articles by:
    - `status`: Status of the article (e.g., 'Draft', 'Published').
    """,
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
def get_articles_by_status(status: Optional[ArticleStatus] = None,article_service:ArticleService=Depends()):
    try:
        articles = article_service.get_articles_by_status(status)
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
            for article in articles
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Get a single Article (Admin,Editor) ",
    description="""
    Fetches the details of a single article by its ID.
    Only Admins and Editors can access this endpoint.
    """,
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
def get_article(article_id: UUID,article_service:ArticleService=Depends()):
    try:
        article=article_service.get_article_by_id(article_id)
        return ArticleResponse(
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.put(
    "/{article_id}",
    response_model=ArticleResponse,
    summary="Update article  By:(Author,Admin,Editor)",
    description="""
    Allows updating an article by its ID. 
    - Authors can update only their own articles.
    - Admins and Editors can update any article.
    """,
    dependencies=[Depends(require_role(["Admin", "Editor","Author"]))],

)
async def update_article(article_id: UUID, article_update: ArticleUpdate,article_service:ArticleService=Depends()):
    try:
        update_article=article_service.update_article(article_id,article_update)
        return ArticleResponse(
            id=update_article.id,
            title=update_article.title,
            content=update_article.content,
            tags=[tag.name for tag in update_article.tags],
            category=update_article.category.name,
            status=update_article.status,
            author=update_article.author.username,
            created_at=update_article.created_at,
            updated_at=update_article.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/{article_id}",
    response_model=dict,
    summary="Delete an Article (Admin,Editor)",
    description="""
    Deletes an article by its ID. Only Admins and Editors can perform this action.
    """,
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
async def delete_article(article_id: UUID,article_service:ArticleService=Depends()):
    try:
        article_service.delete_article(article_id)
        return {
            "message": "Article deleted successfully",
            "article_id": str(article_id)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{article_id}/status",
    response_model=ArticleResponse,
    summary="Update article status  By only:(Admin,Editor)",
    description="""
    Updates the status of an article 
    (e.g., 'Draft', 'In Review', 'Published', 'Rejected').
    Only Admins and Editors are allowed to perform this action.
    """,
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
def update_article_status(article_id: UUID, status_update: ArticleStatusUpdate,article_service:ArticleService=Depends()):
    try:
        article_updated=article_service.update_article_status(article_id,status_update.status)
        return ArticleResponse(
            id=article_updated.id,
            title=article_updated.title,
            content=article_updated.content,
            tags=[tag.name for tag in article_updated.tags],
            category=article_updated.category.name,
            status=article_updated.status,
            author=article_updated.author.username,
            created_at=article_updated.created_at,
            updated_at=article_updated.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
    "/{article_id}/publish",
    summary="Publish Article",
    response_model=ArticleResponse,
    description="Allows editors and admins to change the status of an article to 'Published'.",
    dependencies=[Depends(require_role(["Admin", "Editor"]))],
)
def publish_article(
    article_id: UUID,
    article_service:ArticleService=Depends()
):
    try:
        article=article_service.update_article_status(article_id,ArticleStatus.PUBLISHED)
        return ArticleResponse(
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))






