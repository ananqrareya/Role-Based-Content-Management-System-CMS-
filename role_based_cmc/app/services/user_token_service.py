from datetime import datetime

from sqlalchemy.sql.functions import current_time

from app.entities.models import UserTokens
from app.repositories import user_repository
from app.repositories.user_repository import UserRepository
from app.repositories.user_token_repository import UserTokenRepository

import jwt
class UserTokenService:
    def __init__(self,token_repository:UserTokenRepository,user_repository:UserRepository=None):
        self.token_repository = token_repository
        self.user_repository = user_repository

    def store_user_token(self, user_id, token,expires_at):

        user_token=UserTokens(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_active=True
        )
        self.token_repository.save_token(user_token)

    def get_token_is_active(self, token:str):
        token_active=self.token_repository.get_token_is_active(token)
        if not token_active:
            return None
        return token_active


    def deactivate_expired_tokens(self,username:str):
        current_time=datetime.utcnow()
        current_user=self.user_repository.get_user_by_username(username)
        if not current_user:
            raise ValueError(f"User with username '{username}' not found")
        self.token_repository.deactivate_expired_token_of_user(current_user,current_time)

    def revoke_token(self,token:str):
        token_in_db =self.token_repository.get_token_is_active(token)
        if not user_token:
            raise ValueError(f"User with token '{token}' not found")
        else:
            self.token_repository.revoke(token_in_db )
