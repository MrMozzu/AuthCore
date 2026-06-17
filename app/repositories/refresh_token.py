from app.extensions import db
from app.models.refresh_token import RefreshToken

class RefreshTokenRepository:

    @staticmethod
    def revoke_all_user_sessions(user_id):

        try:
            RefreshToken.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            return True
        except:
            db.session.rollback()
            raise Exception("Error while revoking sessions")
    