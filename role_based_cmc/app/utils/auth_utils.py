import jwt
from datetime import datetime, timedelta, timezone
from starlette.requests import Request
from fastapi import HTTPException
from app.core.config import settings
from app.services.user_service import UserService
from app.services.user_token_service import UserTokenService


def create_access_token(
    data: dict, user_service: UserService, user_token_service: UserTokenService
):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    user = user_service.get_user_by_username(data["sub"])

    user_token_service.store_user_token(user.id, encoded_jwt, expire)

    return encoded_jwt


def get_token_from_request(request: Request):
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        raise HTTPException(status_code=401,
                            detail="Missing Authorization header")
    parts = authorization_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401, detail="Invalid Authorization header format"
        )
    return parts[1]


def verify_access_token(request: Request,
                        user_token_service: UserTokenService):

    token = get_token_from_request(request)
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        token_in_db = user_token_service.get_token_active(token)

        if not token_in_db or token_in_db.expires_at < datetime.now(
            timezone.utc
        ).replace(tzinfo=None):
            raise HTTPException(status_code=401,
                                detail="Invalid or expired token")

        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error during token verification"
        )
