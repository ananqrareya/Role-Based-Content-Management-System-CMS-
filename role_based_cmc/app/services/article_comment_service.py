

from fastapi.params import Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.entities.models import Comments, Articles
from app.repositories.article_comment_repository import (ArticleCommentRepository)
from app.services.article_service import ArticleService


class ArticleCommentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.article_comment_repository = ArticleCommentRepository(db)
        self.article_service = ArticleService(db)

    def new_comment(self, article_id: UUID, comment: str, user_id: str):
        try:
            user_id = UUID(user_id)
            article = self.article_service.get_article_by_id(article_id)
            if article is None:
                raise ValueError(f"article with id"
                                 f" {article_id} does not exist")

            comment_article = Comments(
                article_id=article_id,
                user_id=user_id,
                content=comment,
            )
            save_comment = (self.article_comment_repository
                            .save_comment(comment_article))
            return save_comment
        except Exception as e:
            raise e

    def get_article_with_comment(self, article_id: UUID) -> Articles:
        try:
            article = self.article_service.get_article_by_id(article_id)
            if article is None:
                raise ValueError(f"article with id "
                                 f"{article_id} does not exist")
            return article
        except Exception as e:
            raise e

    def update_comment(self, comment_id: UUID, comment_text: str):
        try:
            comment_db = (self.article_comment_repository
                          .get_comment_by_id(comment_id))
            if comment_db is None:
                raise ValueError(f"comment with id "
                                 f"{comment_id} does not exist")
            update_comment = self.article_comment_repository.update_comment(
                comment_db, comment_text
            )
            return update_comment
        except Exception as e:
            raise e

    def delete_comment(self, comment_id: UUID):
        comment_db = (self.article_comment_repository
                      .get_comment_by_id(comment_id))
        if comment_db is None:
            raise ValueError(f"comment with id {comment_id} does not exist")
        self.article_comment_repository.delete_comment(comment_db)
        return comment_db
