from sqlalchemy import Column, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Roles(Base):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String)


    users = relationship("User", back_populates="role")
