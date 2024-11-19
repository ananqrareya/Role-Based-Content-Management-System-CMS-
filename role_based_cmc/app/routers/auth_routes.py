from fastapi import APIRouter

from app.schemas.auth_schema import LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", summary="Login user", response_model=LoginResponse)
def login_user(user: LoginRequest):
    pass
