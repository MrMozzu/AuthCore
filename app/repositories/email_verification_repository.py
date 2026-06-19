from app.extensions import db 

class EmailVerificationRepository:

    @staticmethod
    def create_token(token_hash, user_id, expires_at):
        token = EmailVerification(token_hash=token_hash, user_id=user_id, expires_at=expires_at)
        db.session.add(token)
        db.session.commit()
        

    
    @staticmethod
    def find_by_token(token_hash):
        token = EmailVerification.query.filter_by(token_hash=token_hash).first()
        return token


    @staticmethod
    def invalidate_user_tokens(user_id):
        tokens = EmailVerification.query.filter_by(user_id=user_id).all()
        for token in tokens:
            token.is_used = True
        db.session.commit()


    @staticmethod
    def mark_used(token):
        token.is_used = True
        db.session.commit()
        
