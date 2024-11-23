from sqlalchemy import Column, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class ArticleTags(Base):
    __tablename__ = 'article_tags'


    article_id = Column(UUID(as_uuid=True), ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    tag_id = Column(UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


    __table_args__ = (
        PrimaryKeyConstraint('article_id', 'tag_id'),
    )
