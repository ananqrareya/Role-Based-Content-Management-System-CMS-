

from sqlalchemy import (
    Column, String, Text, Enum, ForeignKey, TIMESTAMP, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Articles(Base):
    __tablename__ = 'articles'
    id = Column(UUID(as_uuid=True), primary_key=True,  server_default=func.gen_random_uuid() )
    title = Column(String(55), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    status = Column(
        Enum('Draft', 'In Review', 'Published', 'Rejected', name='article_status'),
        nullable=False,
        default='Draft'
    )
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    author = relationship("User", back_populates="articles")
    category = relationship("Categories", back_populates="articles")
    tags = relationship("Tags", secondary="article_tags", back_populates="articles")
    comments = relationship("Comments", back_populates="article", cascade="all, delete-orphan")

