from sqlalchemy import func, Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String(55), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    articles = relationship("Articles", back_populates="category", cascade="all, delete-orphan")
