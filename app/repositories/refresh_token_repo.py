from app.extensions import db
from app.models.user import User
from app.models.refresh_token import RefreshToken

class RevokedTokenRepository():

    @staticmethod
    def create_token(jti, user_id, token_type, expires_at):
        token = RefreshToken(jti=jti, user_id=user_id, token_type=token_type, expires_at=expires_at)
        try:
            db.session.add(token)
            db.session.commit()
            return token
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error while creating token: {str(e)}")
    
    @staticmethod
    def get_token(jti):
        return RefreshToken.query.filter_by(jti=jti).first()