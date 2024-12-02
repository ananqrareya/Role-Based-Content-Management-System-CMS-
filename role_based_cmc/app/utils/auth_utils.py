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


def create_access_token(data: dict, session:Session):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    user_token_repository = UserTokenRepository(session)
    user_token_service = UserTokenService(user_token_repository)
    user_repository = UserRepository(session)
    user_service = UserService(user_repository,None)
    user=user_service.get_user_by_username(data['sub'])
    user_token=user_token_service.store_user_token(user.id,encoded_jwt,expire)

    return encoded_jwt

def verify_access_token(token: str,db:Session):
    try:
        user_token_repository = UserTokenRepository(session)
        user_token_service = UserTokenService(user_token_repository)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_in_db=user_token_service.get_token_is_active(payload)
        if not token_in_db or token_in_db.expires_at<datetime.utcnow():
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
