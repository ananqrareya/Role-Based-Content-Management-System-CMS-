from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.entities.schemas.user_schema import (
    UserUpdateResponse,
    UserUpdateRequest,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", summary="Register new user",
             response_model=RegisterResponse)
async def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    if user.role in ["Admin", "Editor"]:
        raise HTTPException(
            status_code=403, detail="You cannot register for this role."
        )
    user_repository = UserRepository(db)
    role_repository = RoleRepository(db)
    user_service = UserService(user_repository, role_repository)
    try:
        registered_user = user_service.register_user(user)
        message = "User registered successfully"
        if registered_user.role.name == "Author":
            message = ("Wait for the admin's approval "
                       "to be able to enjoy the role's privileges")
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
)
def update_user_role(user_id: int, user: UserUpdateRequest):
    pass


@router.get(
    "/", summary="List all users Role (Admin Only)", response_model=List[UserResponse]
)
def get_users():
    pass


@router.get(
    "/{user_id}",
    summary="Get a specific user Role (Admin Only)",
    response_model=UserResponse,
)
def get_user(user_id: int):
    pass
