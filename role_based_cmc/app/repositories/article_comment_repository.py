

from sqlalchemy.orm import Session, joinedload

from app.entities.models import Comments

from uuid import UUID


class ArticleCommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_comment(self, comment: Comments) -> Comments:
        try:
            self.db.add(comment)
            self.db.commit()
            self.db.refresh(comment)
            return comment
        except Exception as e:
            self.db.rollback()
            raise e

    def get_comment_by_id(self, id: UUID) -> Comments:
        return self.db.query(Comments).filter_by(id=id).first()

    def update_comment(self, comment: Comments, comment_text: str) -> Comments:
        try:
            comment.content = comment_text
            self.db.commit()
            self.db.refresh(comment)
            return comment
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_comment(self, comment: Comments) -> Comments:
        try:
            comment = (
                self.db.query(Comments)
                .options(joinedload(Comments.user),
                         joinedload(Comments.article))
                .filter(Comments.id == comment.id)
                .first()
            )
            if comment is None:
                raise ValueError("Comment does not exist.")

            self.db.delete(comment)
            self.db.commit()

            return comment
        except Exception as e:
            raise e
