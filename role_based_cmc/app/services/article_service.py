from datetime import datetime
from typing import Optional, List

from docutils.nodes import title
from fastapi import HTTPException
from fastapi.params import Depends
from requests import delete
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.entities.enums.article_status import ArticleStatus
from app.entities.models import Articles, Categories
from app.entities.schemas.article_schema import ArticleUpdate, ArticleResponse
from app.repositories.article_repository import ArticleRepository
from app.entities.models.Tags import Tags
from uuid import UUID

from app.repositories.categories_repository import CategoriesRepository
from app.repositories.tags_repository import TagsRepository
from app.repositories.user_repository import UserRepository



class ArticleService:
    def __init__(self,db:Session=Depends(get_db)):
        self.db=db
        self.article_repository=ArticleRepository(db)
        self.tags_repository=TagsRepository(db)
        self.categories_repository=CategoriesRepository(db)
        self.user_repository=UserRepository(db)

    def check_tag_name_with_aritcle(self,tag_name:str)->Tags:
        tag=self.tags_repository.get_tag_by_name(tag_name)
        if tag is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Tag '{tag_name}' not found")
        return tag

    def check_category_name_with_article(self,category_name:str)->Categories:
        category=self.categories_repository.get_category_by_name(category_name)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Category '{category_name}' not found")
        return category







    def create_article(self,article:dict)->Articles:
        new_article=Articles(
            title=article['title'],
            content=article['content'],
            author_id=article['author_id'],
            category_id=article['category_id'],
            status=ArticleStatus.DRAFT,
            tags=article["tags"]
        )
        return self.article_repository.add_article(new_article)


    def get_articles_by_status(self,status:Optional[ArticleStatus]=None)->List[Articles]:
        if status==None:
           return self.article_repository.get_all_articles()

        return self.article_repository.get_article_by_status(status)

    def get_article_by_id(self,id:UUID)->Articles:
        article=self.article_repository.get_article_by_id(id)
        if article is None:
            raise HTTPException(status_code=404,detail=f"Article '{id}' not found")
        return article

    def update_article(self,article_id:UUID,article_update:ArticleUpdate)->Articles:
        current_article=self.article_repository.get_article_by_id(article_id)
        if current_article is None:
            raise HTTPException(status_code=404,detail=f"Article '{article_id}' not found")
        article_db=self.article_repository.update_article(current_article,article_update)

        return article_db

    def delete_article(self,id:UUID)->Articles:
        current_article=self.article_repository.get_article_by_id(id)
        if current_article is None:
            raise HTTPException(status_code=404,detail=f"Article '{id}' not found")
        self.article_repository.delete_article(current_article)
        return current_article

    def update_article_status(self,article_id:UUID,article_status:ArticleStatus)->Articles:

        current_article=self.article_repository.get_article_by_id(article_id)
        if current_article is None:
            raise HTTPException(status_code=404,detail=f"Article '{id}' not found")

        updated_article=self.article_repository.update_article_status(current_article,article_status)
        return updated_article

    def submit_article(self,article:Articles,status:ArticleStatus):
        submit_article=self.article_repository.submit_article(article,status)
        return submit_article

    def search_articles(
            self, categories: Optional[List[str]], tags: Optional[List[str]], keyword: Optional[str]
    ) -> List[ArticleResponse]:
        try:

            published_articles = self.article_repository.get_article_by_status(status=ArticleStatus.PUBLISHED)


            if categories:
                published_articles = [
                    article for article in published_articles if str(article.category_id) in categories
                ]


            if tags:
                published_articles = [
                    article for article in published_articles if any(str(tag.id) in tags for tag in article.tags)
                ]


            if keyword:
                published_articles = [
                    article for article in published_articles if
                    keyword.lower() in article.title.lower() or keyword.lower() in article.content.lower()
                ]


            return [
                ArticleResponse(
                    id=article.id,
                    title=article.title,
                    content=article.content,
                    tags=[tag.name for tag in article.tags],
                    category=article.category.name if article.category else None,
                    status=article.status,
                    author=article.author.username,
                    created_at=article.created_at,
                    updated_at=article.updated_at,
                )
                for article in published_articles
            ]

        except Exception as e:
            raise ValueError(f"An error occurred while searching articles: {str(e)}")

    def filter_article(self,author:str, date: Optional[str] = None)->List[ArticleResponse]:
        try:
            published_articles = self.article_repository.get_article_by_status(status=ArticleStatus.PUBLISHED)

            if author:
                published_articles = [
                    article for article in published_articles if(article.author.username == author)
                ]

            if date:
                filter_date = datetime.strptime(date, '%Y-%m-%d').date()
                published_articles = [
                    article for article in published_articles if article.created_at.date()==filter_date
                ]

            return [
                ArticleResponse(
                    id=article.id,
                    title=article.title,
                    content=article.content,
                    tags=[tag.name for tag in article.tags],
                    category=article.category.name if article.category else None,
                    status=article.status,
                    author=article.author.username,
                    created_at=article.created_at,
                    updated_at=article.updated_at,
                )
                for article in published_articles
            ]
        except Exception as e:
            raise ValueError(f"An error occurred while filtering articles: {str(e)}")