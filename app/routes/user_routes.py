from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.schemas.user_schema import UpdateUserSchema, ChangePasswordSchema, UserSchema, UpdateRoleSchema
from app.schemas.response_schema import MessageResponseSchema
from flask_smorest import Blueprint
from app.extensions import limiter
from app.utils.permissions import permission_required, ROLE_PERMISSIONS

users_bp = Blueprint("users", __name__, url_prefix="/users", description="User Management APIs")

@users_bp.get("/me")
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.response(200, UserSchema)
@jwt_required()
@permission_required("view_own_user")
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
        "role": user.role
    }), 200



@users_bp.patch("/update")
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.arguments(UpdateUserSchema)
@users_bp.response(200, UserSchema)
@jwt_required()
@permission_required("update_own_user")
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
        "role": updated_user.role
    }), 200    
    

@users_bp.patch("/change-password")
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.arguments(ChangePasswordSchema)
@users_bp.response(200, MessageResponseSchema)
@jwt_required()
@permission_required("update_own_user")
@limiter.limit("5 per minute")
def change_password(data):

    user_id = get_jwt_identity()

    updated_user = UserService.update_password(user_id, **data)
    
    return jsonify({
        "success": True,
        "message": "Password updated successfully"
    }), 200


@users_bp.get("")
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.response(200, UserSchema(many=True))
@jwt_required()
@permission_required("view_all_users")
def get_all_users():
    users = UserService.get_all_users()
    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "phone_no": user.phone_no,
            "is_verified": user.is_verified,
            "role": user.role
        } for user in users
    ]), 200


@users_bp.patch("/<int:user_id>/role")
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.arguments(UpdateRoleSchema)
@users_bp.response(200, MessageResponseSchema)
@jwt_required()
@permission_required("change_user_role")
def change_user_role(data, user_id):
    UserService.change_user_role(user_id, data["role"])
    return jsonify({
        "success": True,
        "message": f"User role updated to {data['role']} successfully"
    }), 200


@users_bp.delete("/<int:user_id>")
@users_bp.doc(security=[{"BearerAuth": []}])
@users_bp.response(200, MessageResponseSchema)
@jwt_required()
@permission_required("delete_own_user", "delete_any_user")
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if int(current_user_id) != user_id:
        current_user = UserService.get_current_user(current_user_id)
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
        if "delete_any_user" not in user_permissions:
            return jsonify({
                "success": False,
                "message": "You do not have permission to delete this user"
            }), 403

    UserService.delete_user(user_id)
    return jsonify({
        "success": True,
        "message": "User deleted successfully"
    }), 200



