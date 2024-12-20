from typing import List


from fastapi import APIRouter, HTTPException
from uuid import UUID

from fastapi.params import Depends

from app.entities.schemas.role_schema import (
    RoleSchema,
    RoleWithUsersSchema,
    UserSchema,
)

from app.services.roles_service import RoleService
from app.utils.fastapi.dependencies import require_role

router = APIRouter(dependencies=[Depends(require_role(["Admin"]))])


@router.get("/", response_model=List[RoleSchema])
async def get_roles(role_service: RoleService = Depends()):
    try:
        roles = role_service.get_all_role()
        return [
            RoleSchema(id=role.id,
                       name=role.name,
                       description=role.description)
            for role in roles
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/{role_id}/users/",
    response_model=RoleWithUsersSchema,
    summary="get role with users",
)
async def get_role_with_users(role_id: UUID,
                              role_service: RoleService = Depends()):
    try:

        role = role_service.get_role_with_users(role_id)
        return RoleWithUsersSchema(
            role=RoleSchema(
                id=role.id,
                name=role.name,
                description=role.description,
            ),
            users=[
                UserSchema(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                )
                for user in role.users
            ],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
