from datetime import datetime

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.entities.models import UserTokens
from app.repositories.user_repository import UserRepository
from app.repositories.user_token_repository import UserTokenRepository


class UserTokenService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.user_repository = UserRepository(db)
        self.token_repository = UserTokenRepository(db)

    def store_user_token(self, user_id, token, expires_at):
        try:
            user_token = UserTokens(
                user_id=user_id, token=token,
                expires_at=expires_at, is_active=True
            )
            saved_token = self.token_repository.save_token(user_token)
            print(f"Token stored for user {user_id}:"
                  f" {saved_token.token[:20]}...")
            return saved_token
        except Exception as e:
            print(f"Error saving token for user {user_id}: {str(e)}")
            raise

    def get_token_active(self, token: str):
        token_active = self.token_repository.get_token_is_active(token)
        if not token_active:
            return None
        return token_active

    def deactivate_expired_tokens(self, username: str):
        current_time = datetime.utcnow()
        current_user = self.user_repository.get_user_by_username(username)
        if not current_user:
            raise ValueError(f"User with username '{username}' not found")
        self.token_repository.deactivate_expired_token_of_user(
            current_user, current_time
        )

    def revoke_token(self, token: str):
        token_in_db = self.token_repository.get_token_is_active(token)
        if not token_in_db:
            raise ValueError(f"User with token '{token}' not found")
        else:
            self.token_repository.revoke(token_in_db)
