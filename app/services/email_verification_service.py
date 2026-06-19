from app.extensions import db 
from app.models.email_verification_model import EmailVerification 
from app.repositories.email_verification_repository import EmailVerificationRepository
from app.models.user import User
from datetime import datetime 
from hashlib import sha256
import secrets


class EmailVerificationService:

    @staticmethod
    def send_verification_email(): # this function will generate a token and send it to the user's email address 

        token = secrets.token_urlsafe(20) # generates a random string of 20 bytes, then encodes it using urlsafe base64
        token_hash = sha256(token.encode()).hexdigest()  
        expires_at = datetime.now() + timedelta(minutes=10)

        EmailVerificationRepository.create_token(token_hash, user_id, expires_at)

        link = f"http://localhost:3000/auth/verify-email?token={token}"

        msg = Message(subject="Verify your email", sender=current_app.config["MAIL_DEFAULT_SENDER"], recipients=[email])
        # msg.html = render_template("email_templates/verify_email.html", token=token, link=link)
        mail.send(msg)
        
        return True 


    @staticmethod
    def verify_email(token):

        token_hash = sha256(
            token.encode()
        ).hexdigest()

        verification_token = (
            EmailVerificationRepository
            .find_by_token(token_hash)
        )

        if not verification_token:
            return False

        if verification_token.is_used:
            return False

        if verification_token.expires_at < datetime.utcnow():
            return False

        verification_token.user.is_verified = True
        verification_token.is_used = True


        EmailVerificationRepository.invalidate_user_tokens(
            verification_token.user_id
        )

        db.session.commit()

        return True
        
        


