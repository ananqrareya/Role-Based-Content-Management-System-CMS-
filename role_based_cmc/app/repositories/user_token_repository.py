from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func

from sqlalchemy.orm import Session

from app.entities.models import UserTokens
from app.entities.models import User


class UserTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_token(self, token: UserTokens):
        try:
            self.db.add(token)
            self.db.commit()
            self.db.refresh(token)
            print(
                f"Token successfully saved: {token.token[:20]}..."
            )  # Log for confirmation

            return token
        except Exception as e:
            print(f"Error while saving token to database: {str(e)}")
            self.db.rollback()
            raise e

    def get_token_is_active(self, token: str):
        try:
            token_active = (
                self.db.query(UserTokens)
                .filter(UserTokens.token == token,
                        UserTokens.is_active == True)
                .first()
            )
            if not token_active:
                print(f"No active token found for: {token[:20]}...")
            else:
                print(f"Active token retrieved: {token_active.token[:20]}...")
            return token_active
        except Exception as e:
            print(f"Error retrieving active token: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))

    def deactivate_expired_token_of_user(self, user: User,
                                         current_time: datetime):
        self.db.query(UserTokens).filter(
            UserTokens.user_id == user.id,
            UserTokens.expires_at < func.now(),
            UserTokens.is_active == True,
        ).delete(synchronize_session=False)
        self.db.commit()

    def revoke(self, token_in_db: UserTokens):
        token_in_db.is_active = False
        self.db.commit()
