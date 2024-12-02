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
            return token
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_token_is_active(self,token:str):
        return self.db_session.query(UserTokens).filter_by(token=token, is_active=True).first()

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
