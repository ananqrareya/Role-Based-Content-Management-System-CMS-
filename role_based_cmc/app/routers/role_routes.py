from typing import List

from fastapi import APIRouter
from uuid import UUID

from app.schemas.permission_schema import PermissionBase
from app.schemas.role_schema import (
    RoleResponse,
    RoleUpdateRequest,
    RoleCreateRequest,
)

router = APIRouter()


@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreateRequest):
    pass


@router.put(
    "/",
    response_model=RoleResponse,
    description="Update the role's name or description. "
                "At least one field must be provided in the request body.",
)
def update_role(role: RoleUpdateRequest):
    pass


@router.get("/", response_model=List[RoleResponse])
def get_roles():
    pass


@router.delete("/{role_id}", response_model=RoleResponse)
def delete_role(role_id: int):
    pass


@router.put(
    "/{role_id}/permissions",
    response_model=RoleResponse,
    summary="Assign permissions to a role",
)
def assign_permissions(role_id: UUID, permissions: List[PermissionBase]):
    pass


@router.delete("/{role_id}/permissions/", response_model=RoleResponse)
def delete_permissions(role_id: UUID):
    pass
