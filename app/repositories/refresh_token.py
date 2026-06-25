from datetime import datetime
from app.extensions import db
from app.models.refresh_token import RefreshToken

class RefreshTokenRepository:

    @staticmethod 
    def create_token(user_id, jti, expires_at):
        token = RefreshToken(user_id=user_id, jti=jti, expires_at=expires_at)
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

    
    @staticmethod
    def revoke_token(token_id):
        token = RefreshToken.query.filter_by(jti=token_id).first()
        try:
            if token:
                token.is_revoked = True
                token.revoked_at = datetime.utcnow()
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error while revoking token: {str(e)}")

    @staticmethod
    def get_active_tokens_by_user_id(user_id):
        return RefreshToken.query.filter_by(user_id=user_id, is_revoked=False).all()

    @staticmethod
    def revoke_all_by_user_id(user_id):
        try:
            tokens = RefreshToken.query.filter_by(user_id=user_id, is_revoked=False).all()
            for token in tokens:
                token.is_revoked = True
                token.revoked_at = datetime.utcnow()
            db.session.commit()
            return tokens
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error while revoking all user tokens: {str(e)}")

