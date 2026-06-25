from app.extensions import db
from app.models.revoked_token import RevokedToken

class RevokedTokenRepository():

    @staticmethod
    def create_token(jti, user_id, token_type, expires_at):
        token = RevokedToken(jti=jti, user_id=user_id, token_type=token_type, expires_at=expires_at)
        try:
            db.session.add(token)
            db.session.commit()
            return token
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error while creating token: {str(e)}")

    @staticmethod
    def revoke_tokens_bulk(tokens_data):
        try:
            for item in tokens_data:
                token = RevokedToken(
                    jti=item["jti"],
                    user_id=item["user_id"],
                    token_type=item["token_type"],
                    expires_at=item["expires_at"]
                )
                db.session.add(token)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error while revoking tokens in bulk: {str(e)}")