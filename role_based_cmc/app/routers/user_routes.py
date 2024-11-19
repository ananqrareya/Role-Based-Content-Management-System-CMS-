from typing import List

from fastapi import APIRouter


from app.schemas.user_schema import (
    UserUpdateResponse,
    UserUpdateRequest,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
)

router = APIRouter()


@router.post("/register",
             summary="Register new user",
             response_model=RegisterResponse)
def register_user(user: RegisterRequest):
    pass


@router.put(
    "/{user_id}/role",
    summary="Update User Role (Admin Only)",
    response_model=UserUpdateResponse,
)
def update_user_role(user_id: int, user: UserUpdateRequest):
    pass


@router.get(
    "/",
    summary="List all users Role (Admin Only)",
    response_model=List[UserResponse]
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
