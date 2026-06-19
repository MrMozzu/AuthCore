from datetime import datetime
from app.extensions import db
from app.models.mixins.timestampmixin import TimeStampMixin

class RefreshToken(TimeStampMixin, db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    jti = db.Column(db.String, nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", backref="refresh_tokens")
