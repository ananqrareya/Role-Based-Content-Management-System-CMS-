from datetime import datetime

from anyio import current_time
from sqlalchemy.orm import Session
from sqlalchemy.orm.sync import update

from app.entities.models import UserTokens
from app.entities.models import User

class UserTokenRepository:
    def __init__(self,db_session:Session):
        self.db_session = db_session


    def save_token(self,token :UserTokens):
        try:
            self.db_session.add(token)
            self.db_session.commit()
            self.db_session.refresh(token)
            print(f"Token successfully saved: {token.token[:20]}...")  # Log for confirmation

            return token
        except Exception as e:
            print(f"Error while saving token to database: {str(e)}")
            self.db_session.rollback()
            raise e

    def get_token_is_active(self,token:str):
        try:
            token_active = self.token_repository.get_token_is_active(token)
            if not token_active:
                print(f"No active token found for: {token[:20]}...")
            else:
                print(f"Active token retrieved: {token_active.token[:20]}...")
            return token_active
        except Exception as e:
            print(f"Error retrieving active token: {str(e)}")
            raise

    def deactivate_expired_token_of_user(self,user:User,current_time:datetime):
        self.db_session.query(UserTokens).filter(
            UserTokens.user_id==user.id,
            UserTokens.expires_at<current_time,
            UserTokens.is_active==True
        ).update({"is_active":False})
        self.db_session.commit()

    def revoke(self,token_in_db :UserTokens):
        token_in_db .is_active=False
        self.db_session.commit()
