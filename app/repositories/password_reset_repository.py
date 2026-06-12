from datetime import datetime 
from app.models.password_reset_token import PasswordResetToken

class PasswordResetRepository:
    @staticmethod 
    def create_token(user_id: int, token_hash: str, expires_at: datetime) -> PasswordResetToken | None:
        pass

    @staticmethod
    def get_by_token_hash(token_hash:str) -> PasswordResetToken | None:
        pass

    @staticmethod
    def invalidate_token(user_id: int) ->  None:
        pass

    @staticmethod
    def marked_used(token: PasswordResetToken) -> None:
        pass 


