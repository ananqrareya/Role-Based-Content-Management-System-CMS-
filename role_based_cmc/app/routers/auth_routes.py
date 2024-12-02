from os import access

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.entities.schemas.auth_schema import LoginRequest, LoginResponse
from app.repositories.user_token_repository import UserTokenRepository
from app.services.user_service import UserService
from app.services.user_token_service import UserTokenService
from app.utils.auth_utils import create_access_token

router = APIRouter()


@router.post("/login", summary="Login user", response_model=LoginResponse)
async def login_user(user: LoginRequest =Depends() , db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    user_token_repository=UserTokenRepository(db)
    user_token_service = UserTokenService(user_token_repository,user_repository)
    db_user=user_service.authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_token_service.deactivate_expired_tokens(user.username)
    access_token = create_access_token({"sub": db_user.username, "role": db_user.role.name},db)
    return LoginResponse(
        access_token=access_token,
        token_type="bearer"
    )

