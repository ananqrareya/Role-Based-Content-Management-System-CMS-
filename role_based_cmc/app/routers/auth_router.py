from fastapi import APIRouter, HTTPException
from fastapi.params import Depends


from app.entities.schemas.auth_schema import LoginRequest, LoginResponse

from app.services.user_service import UserService
from app.services.user_token_service import UserTokenService
from app.utils.auth_utils import create_access_token

router = APIRouter()


@router.post("/login", summary="Login user", response_model=LoginResponse)
async def login_user(
    user: LoginRequest,
    user_service: UserService = Depends(),
    user_token_service: UserTokenService = Depends(),
):

    db_user = user_service.authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_token_service.deactivate_expired_tokens(user.username)
    access_token = create_access_token(
        {
            "sub": db_user.username,
            "role": db_user.role.name,
            "user_id": str(db_user.id),
        },
        user_service,
        user_token_service,
    )
    return LoginResponse(access_token=access_token, token_type="bearer")
