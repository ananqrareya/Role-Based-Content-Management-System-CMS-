from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class RolePermissions(Base):
    __tablename__ = 'permissions_roles'

    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id', ondelete="CASCADE"), primary_key=True)
