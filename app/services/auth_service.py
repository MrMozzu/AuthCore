from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.revoked_token import RevokedTokenRepository
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token, get_jwt, get_jwt_identity
from app.services.email_service import EmailService
from app.repositories.password_reset_repository import PasswordResetRepository
import secrets
from datetime import datetime, timedelta
from hashlib import sha256
from app.errors.exceptions import ResourceNotFoundError, InvalidCredentialsError, EmailNotVerifiedError, ConflictError, UserNotFoundError, APIException, Unauthorized

class AuthService:

    @staticmethod
    def register(name, username, email, phone_no, password, confirm_password):

        if password != confirm_password:
            raise APIException("Passwords do not match")

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
            raise UserNotFoundError("Invalid credentials")

        if not check_password_hash(user.password_hash, password):
            raise InvalidCredentialsError("Invalid credentials")
        
        if not user.is_verified:
            raise EmailNotVerifiedError("User not verified")

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        decoded_token = decode_token(refresh_token) # this will return payload of the token 

        RefreshTokenRepository.create_token(
            jti=decoded_token["jti"],
            user_id=user.id,
            expires_at=datetime.fromtimestamp(
                decoded_token["exp"]
            )
        )
        
        return access_token, refresh_token

        
    @staticmethod
    def refresh_access_token(user_id):

        user = UserRepository.get_by_id(user_id)

        if not user:
            raise UserNotFoundError("User not found")
        
        new_access_token = create_access_token(identity=str(user.id))
        return new_access_token


    @staticmethod
    def forgot_password(email):
        
        user = UserRepository.get_by_email(email)

        if not user:
            raise UserNotFoundError("User not found")

        PasswordResetRepository.invalidate_tokens(user.id)

        token = secrets.token_urlsafe(32)
        hashed_token = sha256(token.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=30)

        PasswordResetRepository.create_token(user.id, hashed_token, expires_at)
        EmailService.send_reset_password_email(user.email, token)
        
        return token 
        
    
    @staticmethod
    def reset_password(token, new_password, confirm_new_password):

        if new_password != confirm_new_password:
            raise APIException("Passwords do not match")

        hashed_token = sha256(token.encode()).hexdigest()
        password_reset_token = PasswordResetRepository.get_by_token_hash(hashed_token)

        user = UserRepository.get_by_id(password_reset_token.user_id)

        if not user:
            raise UserNotFoundError("User not found")
        
        if user.check_password(new_password):
            raise InvalidCredentialsError("New password cannot be same as old password")

        user.set_password(new_password)
        UserRepository.update(user)

        PasswordResetRepository.mark_used(password_reset_token)
        
        return True

        
    @staticmethod
    def refresh_token(user_id):
        
        jwt_data = get_jwt()
        jti = jwt_data["jti"]
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise UserNotFoundError("User not found")
        
        token = RefreshTokenRepository.get_token(jti)

        if not token:
            raise Unauthorized("Refresh token not found")
        
        if token.is_revoked:
            raise Unauthorized("Refresh token is revoked")
        
        RefreshTokenRepository.revoke_token(token.jti)
        RevokedTokenRepository.create_token(
            jti=token.jti,
            user_id=token.user_id,
            token_type="refresh",
            expires_at=token.expires_at
        )

        new_access_token = create_access_token(identity=str(user.id))
        new_refresh_token = create_refresh_token(identity=str(user.id))

        decoded_refresh_token = decode_token(new_refresh_token)

        RefreshTokenRepository.create_token(
            jti=decoded_refresh_token["jti"],
            user_id=user.id,
            expires_at=datetime.fromtimestamp(
                decoded_refresh_token["exp"]
            )
        )

        return new_access_token, new_refresh_token 

    @staticmethod
    def logout(access_token_jwt, refresh_token=None):
        # Revoke the current access token
        access_jti = access_token_jwt["jti"]
        user_id = int(access_token_jwt["sub"])
        access_expires_at = datetime.fromtimestamp(access_token_jwt["exp"])

        RevokedTokenRepository.create_token(
            jti=access_jti,
            user_id=user_id,
            token_type="access",
            expires_at=access_expires_at
        )

        # Revoke the refresh token if provided
        if refresh_token:
            try:
                decoded_refresh = decode_token(refresh_token)
                refresh_jti = decoded_refresh["jti"]
                refresh_user_id = int(decoded_refresh["sub"])
                refresh_expires_at = datetime.fromtimestamp(decoded_refresh["exp"])

                if refresh_user_id != user_id:
                    raise Unauthorized("Refresh token does not belong to the user")

                # Revoke in RefreshToken table
                RefreshTokenRepository.revoke_token(refresh_jti)

                # Also add to RevokedToken blacklist
                from app.models.revoked_token import RevokedToken
                if not RevokedToken.is_revoked(refresh_jti, refresh_user_id, "refresh"):
                    RevokedTokenRepository.create_token(
                        jti=refresh_jti,
                        user_id=refresh_user_id,
                        token_type="refresh",
                        expires_at=refresh_expires_at
                    )
            except Exception as e:
                raise APIException(f"Invalid refresh token: {str(e)}")

    @staticmethod
    def logout_all_devices(access_token_jwt):
        # Revoke the current access token
        access_jti = access_token_jwt["jti"]
        user_id = int(access_token_jwt["sub"])
        access_expires_at = datetime.fromtimestamp(access_token_jwt["exp"])

        RevokedTokenRepository.create_token(
            jti=access_jti,
            user_id=user_id,
            token_type="access",
            expires_at=access_expires_at
        )

        # Revoke all active refresh tokens for this user
        active_tokens = RefreshTokenRepository.get_active_tokens_by_user_id(user_id)
        if active_tokens:
            RefreshTokenRepository.revoke_all_by_user_id(user_id)

            from app.models.revoked_token import RevokedToken
            tokens_to_revoke = []
            for token in active_tokens:
                if not RevokedToken.is_revoked(token.jti, user_id, "refresh"):
                    tokens_to_revoke.append({
                        "jti": token.jti,
                        "user_id": user_id,
                        "token_type": "refresh",
                        "expires_at": token.expires_at
                    })
            if tokens_to_revoke:
                RevokedTokenRepository.revoke_tokens_bulk(tokens_to_revoke)
 