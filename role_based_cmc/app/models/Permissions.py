from sqlalchemy import Column, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Permissions(Base):
    __tablename__ = 'permissions'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    # Relationship with roles through the join table
    roles = relationship(
        "Roles",
        secondary="permissions_roles",  # Name of the join table
        back_populates="permissions"
    )
