from datetime import datetime
from app.extensions import db
from app.models.mixins.timestampmixin import TimeStampMixin

class RevokedToken(TimeStampMixin, db.Model):
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

        # this function checks if the token is revoekd or not by comparing th ejti , user_id and token_type from the request token with the database 
        # if the token matches any token in the database it means the token is revoked 
        # else it is not revoked 
        # i have to make sure user_id is also matched becuase same jti can be used for different users
        # this function is used by the jwt_required to check if the token is revoked or not

        