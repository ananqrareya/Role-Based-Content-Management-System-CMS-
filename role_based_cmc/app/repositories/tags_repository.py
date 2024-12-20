from sqlalchemy.orm import Session
from app.entities.models.Tags import Tags
from uuid import UUID


class TagsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_tag_by_name(self, tag_name: str) -> Tags:
        return self.session.query(Tags).filter_by(name=tag_name).first()

    def get_tag_by_id(self, tag_id: UUID) -> Tags:
        return self.session.query(Tags).get(tag_id)

    def add_tag(self, tag: Tags):
        try:
            self.session.add(tag)
            self.session.commit()
            self.session.refresh(tag)
            return tag
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all_tags(self):
        try:
            return self.session.query(Tags).all()
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_tag(self, tag: Tags):
        try:
            self.session.delete(tag)
            self.session.commit()
            return tag
        except Exception as e:
            self.session.rollback()
            raise e
