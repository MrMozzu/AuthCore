from datetime import datetime
from app.extensions import db

class RevokedToken(db.Model):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    jti = db.Column(db.String, nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    token_type = db.Column(db.String, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)


    @staticmethod
    def is_revoked(jti, user_id, token_type): 
        token = RevokedToken.query.filter_by(jti=jti, user_id=user_id, token_type=token_type).first()
        return token is not None