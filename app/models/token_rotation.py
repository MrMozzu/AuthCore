from app.extensions import db

class TokenRotation(db.Model):
    __tablename__ = "token_rotations"

    id  = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    jti = db.Column(db.String, nullable=False, unique=True)
    parent_jti = db.Column(db.String, nullabel=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    revoked = db.Column(db.Boolean, default=False)
    

