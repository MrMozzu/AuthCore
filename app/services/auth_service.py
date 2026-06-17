from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.exceptions import ConflictError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity
from app.services.email_service import EmailService
from app.repositories.password_reset_repository import PasswordResetRepository
import secrets
from datetime import datetime, timedelta
from hashlib import sha256 

class AuthService:

    @staticmethod
    def register(name, username, email, phone_no, password):

        existing_email = UserRepository.get_by_email(email)
        existing_username = UserRepository.get_by_username(username)
        existing_phone_no = UserRepository.get_by_phone_no(phone_no)

        if existing_email:
            raise ConflictError("Email already registered")

        if existing_username:
            raise ConflictError("username already taken")

        if existing_phone_no:
            raise ConflictError("phone number already registered")
        
        new_user = User(name=name, username=username, email=email, phone_no=phone_no)
        new_user.set_password(password)

        return UserRepository.create(new_user)



    @staticmethod
    def login(email, password):

        user = UserRepository.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")

        if not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid credentials")

        return user

        
    @staticmethod
    def refresh_access_token(user_id):

        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")
        
        new_access_token = create_access_token(identity=str(user.id))
        return new_access_token


    @staticmethod
    def forgot_password(email):
        
        user = UserRepository.get_by_email(email)

        if not user:
            return None 

        PasswordResetRepository.invalidate_tokens(user.id)

        token = secrets.token_urlsafe(32)
        hashed_token = sha256(token.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=30)

        PasswordResetRepository.create_token(user.id, hashed_token, expires_at)
        EmailService.send_reset_password_email(user.email, token)
        return token 
        
    
    @staticmethod
    def reset_password(token, new_password):

        hashed_token = sha256(token.encode()).hexdigest()
        password_reset_token = PasswordResetRepository.get_by_token_hash(hashed_token)

        user = UserRepository.get_by_id(password_reset_token.user_id)

        if not user:
            raise ValueError("User not found")
        
        if user.check_password(new_password):
            raise ValueError("New password cannot be same as old password")

        user.set_password(new_password)
        UserRepository.update(user)

        PasswordResetRepository.mark_used(password_reset_token)
        
        return True

        