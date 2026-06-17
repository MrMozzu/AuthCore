from datetime import datetime
from app.extensions import db 
from app.models.mixins.timestampmixin import TimeStampMixin

class PasswordResetToken(TimeStampMixin, db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    token_hash = db.Column(db.String, nullable=False, index=True)  # index means faster lookups
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship("User", backref="password_reset_tokens")


    

