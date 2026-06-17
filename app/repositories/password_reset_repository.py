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
        password_reset_token = PasswordResetToken.query.filter_by(token_hash=token_hash).first()

        if not password_reset_token or password_reset_token.is_used or password_reset_token.expires_at < datetime.utcnow():
            raise ValueError("Invalid or expired token")

        return password_reset_token
        

    @staticmethod
    def invalidate_tokens(user_id: int) ->  None:
        tokens = PasswordResetToken.query.filter_by(user_id=user_id).all()

        for token in tokens:
            token.is_used = True
        
        db.session.commit()

    @staticmethod
    def mark_used(token: PasswordResetToken) -> None:
        token.is_used = True
        db.session.commit()

    

 

