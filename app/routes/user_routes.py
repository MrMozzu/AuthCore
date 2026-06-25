from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.schemas.user_schema import UpdateUserSchema, ChangePasswordSchema, UserSchema
from app.schemas.response_schema import MessageResponseSchema
from flask_smorest import Blueprint

users_bp = Blueprint("users", __name__, url_prefix="/users", description="User Management APIs")

@users_bp.get("/me")
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.response(200, UserSchema)
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
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.arguments(UpdateUserSchema)
@users_bp.response(200, UserSchema)
@jwt_required()
def update_user(data):

    user_id = get_jwt_identity()
    
    updated_user = UserService.update_user(user_id, **data)
    
    return jsonify({
        "id": updated_user.id,
        "name": updated_user.name,
        "username": updated_user.username,
        "email": updated_user.email,
        "phone_no": updated_user.phone_no,
        "is_verified": updated_user.is_verified,
    }), 200    
    

@users_bp.patch("/change-password")
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.arguments(ChangePasswordSchema)
@users_bp.response(200, MessageResponseSchema)
@jwt_required()
def change_password(data):

    user_id = get_jwt_identity()

    updated_user = UserService.update_password(user_id, **data)
    
    return jsonify({
        "success": True,
        "message": "Password updated successfully"
    }), 200

