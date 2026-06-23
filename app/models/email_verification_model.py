from app.extensions import db 
from app.models.mixins.timestampmixin import TimeStampMixin
from datetime import datetime 
from hashlib import sha256


class EmailVerification(TimeStampMixin, db.Model):
    __tablename__ = "email_verification"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    token_hash = db.Column(db.String, nullable=False, unique=True, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship("User", backref="email_verification_tokens")

    @staticmethod
    def is_verified(token):
        token_hash = sha256(token.encode()).hexdigest()
        verification = EmailVerification.query.filter_by(token_hash=token_hash).first()

        if not verification:
            return False 

        if verification.is_used:
            return False

        if verification.expires_at < datetime.utcnow():
            return False

        return verification