from sqlalchemy import Column, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Comments(Base):
    __tablename__ = 'comments'


    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    article_id = Column(UUID(as_uuid=True), ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)  # Comment content
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


    article = relationship("Articles", back_populates="comments")
    user = relationship("User", back_populates="comments")
