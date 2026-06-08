from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.exceptions import ConflictError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity


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

