from sqlalchemy import Column, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Tags(Base):
    __tablename__ = "tags"
    id = Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=func.gen_random_uuid()
    )
    name = Column(String(55), nullable=False)

    articles = relationship("Articles",
                            secondary="article_tags", back_populates="tags")
