from sqlalchemy import Column, func, String, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=func.gen_random_uuid()
    )
    username = Column(String(55), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed password
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(),
        onupdate=func.now(), nullable=False
    )

    role = relationship("Roles")
    tokens = relationship(
        "UserTokens", back_populates="user", cascade="all, delete-orphan"
    )
    articles = relationship(
        "Articles", back_populates="author", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comments", back_populates="user", cascade="all, delete-orphan"
    )

