from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services.user_service import UserService
from datetime import datetime, timezone
from app.models.revoked_token import RevokedToken
from app.repositories.user_repository import UserRepository

users_bp = Blueprint("user", __name__, url_prefix="/users")

@users_bp.get("/me")
@jwt_required()
def get_me():

    user_id = get_jwt_identity()
    current_user = UserService.get_current_user(user_id)

    if not current_user:
        return jsonify({"error": "User does not exists"}), 400
    
    return jsonify({
        "id": current_user.id,
        "name": current_user.name,
        "username": current_user.username,
        "email": current_user.email,
        "phone_no": current_user.phone_no,
        "is_verified": current_user.is_verified,
    }), 200



@users_bp.patch("/update")
@jwt_required()
def update_user():

    user_id = get_jwt_identity()


    data = request.get_json()

    if not data:
        return jsonify({"error":"Data not found"}), 404
    
    email = data.get("email")
    if not email:
        return jsonify({"error": "Invalid email"}), 400

    phone_no = data.get("phone_no")
    if not phone_no:
        return jsonify({"error": "Invalid phone number"}), 400

    try:
        updated_user = UserService.update_user(user_id, email, phone_no)
        return jsonify({
            "id": updated_user.id,
            "email": updated_user.email,
            "phone_no": updated_user.phone_no,
            "name": updated_user.name,
            "message": "User updated successfully"
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    
@users_bp.patch("/change-password")
@jwt_required()
def change_password():

    user_id = get_jwt_identity()

    data = request.get_json()

    if not data:
        return jsonify({"error": "Data not found"}), 400
    
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    
    if not old_password or not new_password:
        return jsonify({"error": "Please provide both old_password and new_password"}), 400
    
    try:
        UserService.update_password(user_id, old_password, new_password)
        return jsonify({"message": "Password updated successfully"}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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