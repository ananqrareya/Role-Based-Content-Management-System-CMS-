from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.entities.schemas.user_schema import (
    UserUpdateResponse,
    UserUpdateRequest,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
)
from app.services.user_service import UserService

from uuid import UUID

from app.utils.fastapi.dependencies import require_role

router = APIRouter()


@router.post("/register",
             summary="Register new user",
             response_model=RegisterResponse)
async def register_user(user: RegisterRequest,
                        user_service: UserService = Depends()):
    if user.role in ["Admin", "Editor"]:
        raise HTTPException(
            status_code=403, detail="You cannot register for this role."
        )
    try:
        registered_user = user_service.register_user(user)
        message = "User registered successfully"
        if registered_user.role.name == "Author":
            message = (
                "Wait for the admin's approval "
                "to be able to enjoy the role's privileges"
            )
        return RegisterResponse(
            user=UserResponse(
                id=registered_user.id,
                username=registered_user.username,
                email=registered_user.email,
                is_active=registered_user.is_active,
                created_at=registered_user.created_at,
                updated_at=registered_user.updated_at,
                role=registered_user.role.name,
            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/{user_id}/role",
    summary="Update User Role (Admin Only)",
    response_model=UserUpdateResponse,
    dependencies=[Depends(require_role(["Admin"]))],
)
async def update_user_role(
    user_id: UUID, user: UserUpdateRequest,
        user_service: UserService = Depends()
):
    try:
        user = user_service.update_role(user_id, user.role)
        message = "User updated successfully"
        return UserUpdateResponse(
            user=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                role=user.role.name,
            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    summary="List all users Role (Admin Only)",
    response_model=List[UserResponse],
    dependencies=[Depends(require_role(["Admin"]))],
)
async def get_users(user_service: UserService = Depends()):
    try:
        users = user_service.get_all_users()
        return [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                role=user.role.name,
            )
            for user in users
        ]
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{user_id}",
    summary="Get a specific user Role (Admin Only)",
    response_model=UserResponse,
    dependencies=[Depends(require_role(["Admin"]))],
)
async def get_user(user_id: UUID, user_service: UserService = Depends()):
    try:
        user = user_service.get_user_by_id(user_id)
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            role=user.role.name,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/inactive/",
    summary="List all inactive users (Admin Only)",
    response_model=List[UserResponse],
    dependencies=[Depends(require_role(["Admin"]))],
)
async def get_inactive_users(user_service: UserService = Depends()):
    try:

        users_inactive = user_service.get_users_inactive()

        return [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                role=user.role.name,
            )
            for user in users_inactive
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving inactive users: {str(e)}"
        )


@router.put(
    "/{user_id}/active/",
    summary="Activate the Author role user (Admin Only)",
    response_model=UserUpdateResponse,
    dependencies=[Depends(require_role(["Admin"]))],
)
async def activate_author_user(user_id: UUID,
                               user_service: UserService = Depends()):
    try:
        user = user_service.activate_user(user_id)
        message = "User activated successfully"
        return UserUpdateResponse(
            user=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                role=user.role.name,
            ),
            message=message,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
