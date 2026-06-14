from datetime import datetime 
from app.models.password_reset_token import PasswordResetToken
from app.extensions import db

class PasswordResetRepository:
    @staticmethod 
    def create_token(user_id: int, token_hash: str, expires_at: datetime) -> PasswordResetToken | None:
        try:
            new_token = PasswordResetToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)

            db.session.add(new_token)
            db.session.commit()

            return new_token
        
        except Exception as e:
            db.session.rollback()
            raise Exception("Error while creating token") from e

    @staticmethod
    def get_by_token_hash(token_hash:str) -> PasswordResetToken | None:
        pass 


    @staticmethod
    def invalidate_tokens(user_id: int) ->  None:
        pass

    @staticmethod
    def marked_used(token: PasswordResetToken) -> None:
        pass 

 

