from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services.user_service import UserService
from datetime import datetime, timezone
from app.models.revoked_token import RevokedToken
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UpdateUserSchema, ChangePasswordSchema

users_bp = Blueprint("user", __name__, url_prefix="/users")

@users_bp.get("/me")
@jwt_required()
def get_me():

    user_id = get_jwt_identity()
    user = UserService.get_current_user(user_id)
    
    return jsonify({
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "phone_no": user.phone_no,
        "is_verified": user.is_verified,
    }), 200



@users_bp.patch("/update")
@jwt_required()
def update_user():

    user_id = get_jwt_identity()
    
    data = UpdateUserSchema().load(request.get_json())
    updated_user = UserService.update_user(user_id, **data)
    
    return jsonify({
            "id": updated_user.id,
            "email": updated_user.email,
            "phone_no": updated_user.phone_no,
            "name": updated_user.name,
            "message": "User updated successfully"
    }), 200    
    

@users_bp.patch("/change-password")
@jwt_required()
def change_password():

    user_id = get_jwt_identity()

    data = ChangePasswordSchema().load(request.get_json())
    updated_user = UserService.update_password(user_id, **data)
    
    return jsonify({
        "message": "Password updated successfully"
    }), 200


@users_bp.post("/logout")
@jwt_required()
def logout():
    jwt_payload = get_jwt()
    jti = jwt_payload['jti']
    user_id = jwt_payload["sub"]
    token_type = jwt_payload["type"]
    expires_at = datetime.fromtimestamp(jwt_payload["exp"], tz= timezone.utc)
    

    token = RevokedToken(jti=jti, user_id=user_id, expires_at=expires_at, token_type=token_type)
    UserRepository.revoke_token(token)
    
    return jsonify({"message": "User logged out successfully"}), 200