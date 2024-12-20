from typing import List

from sqlalchemy.orm import Session

from app.entities.enums.article_status import ArticleStatus
from app.entities.models import Articles

from uuid import UUID

from app.entities.schemas.article_schema import ArticleUpdate


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_article(self, article: Articles) -> Articles:
        try:
            self.db.add(article)
            self.db.commit()
            self.db.refresh(article)
            return article
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all_articles(self) -> List[Articles]:
        return self.db.query(Articles).all()

    def get_article_by_status(self, status: ArticleStatus) -> List[Articles]:
        return self.db.query(Articles).filter_by(status=status).all()

    def get_article_by_id(self, id: UUID) -> Articles:
        return self.db.query(Articles).filter_by(id=id).first()

    def update_article(
        self, article_db: Articles, article_update: ArticleUpdate
    ) -> Articles:
        try:
            update_data = article_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                if value is not None:
                    setattr(article_db, key, value)
            self.db.commit()
            self.db.refresh(article_db)
            return article_db
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_article(self, article: Articles) -> Articles:
        try:
            self.db.delete(article)
            self.db.commit()
            return article
        except Exception as e:
            self.db.rollback()
            raise e

    def update_article_status(
        self, article: Articles, status: ArticleStatus
    ) -> Articles:
        try:
            article.status = status
            self.db.commit()
            self.db.refresh(article)
            return article
        except Exception as e:
            self.db.rollback()
            raise e

    def submit_article(self, article: Articles,
                       status: ArticleStatus) -> Articles:
        try:
            article.status = status
            self.db.commit()
            self.db.refresh(article)
            return article
        except Exception as e:
            self.db.rollback()
            raise e
