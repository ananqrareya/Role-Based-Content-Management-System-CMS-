from http.client import HTTPException

import jwt
from datetime import datetime, timedelta

import jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.entities.models import UserTokens
from app.repositories.user_repository import UserRepository
from app.repositories.user_token_repository import UserTokenRepository
from app.services.user_service import UserService
from app.services.user_token_service import UserTokenService


def create_access_token(data: dict, session: Session):
    to_encode = data.copy()


    print(f"ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")


    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})

    print(f"Creating token for user: {data['sub']}")
    print(f"Token expires at: {expire}")

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print(f"Generated JWT token: {encoded_jwt[:20]}...")  # Log only part of the token for security

    user_token_repository = UserTokenRepository(session)
    user_token_service = UserTokenService(user_token_repository)
    user_repository = UserRepository(session)
    user_service = UserService(user_repository, None)
    user = user_service.get_user_by_username(data['sub'])

    user_token = user_token_service.store_user_token(user.id, encoded_jwt, expire)
    print(f"Stored token for user {data['sub']} in the database, expires at {expire}")

    return encoded_jwt

def verify_access_token(token: str, db: Session):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            leeway=10
        )
        print(f"Decoded token payload: {payload}")

        user_token_repository = UserTokenRepository(db)
        user_token_service = UserTokenService(user_token_repository)
        token_in_db = user_token_service.get_token_is_active(token)

        print("token in db:",token_in_db)
        if not token_in_db or token_in_db.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        print(f"Token for user {payload['sub']} is valid.")
        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    except Exception as exc:
        print(f"Unexpected error during token verification: {str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error during token verification")
