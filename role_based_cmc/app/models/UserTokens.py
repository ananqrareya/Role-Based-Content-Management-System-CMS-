
from sqlalchemy import Column, func, TIMESTAMP, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class UserTokens(Base):
    __tablename__ = 'user_tokens'
    id=Column(UUID(as_uuid=True), primary_key=True,server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    token = Column(Text, nullable=False)
    issued_at = Column(TIMESTAMP, nullable=False,server_default=func.now())
    expires_at=Column(TIMESTAMP,nullable=False)
    is_active=Column(Boolean,default=True,nullable=False)
    user = relationship("User", back_populates="tokens")

