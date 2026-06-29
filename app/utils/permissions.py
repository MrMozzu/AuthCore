from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User

ROLE_PERMISSIONS = {
    "user": [
        "view_own_user",
        "update_own_user",
        "delete_own_user"
    ],
    "moderator": [
        "view_own_user",
        "update_own_user",
        "view_all_users"
    ],
    "admin": [
        "view_own_user",
        "update_own_user",
        "view_all_users",
        "change_user_role",
        "delete_any_user"
    ]
}

def permission_required(*required_permissions):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                return jsonify({
                    "success": False,
                    "message": "Missing or invalid token"
                }), 401

            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user:
                return jsonify({
                    "success": False,
                    "message": "User not found"
                }), 404
            
            user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
            if not any(p in user_permissions for p in required_permissions):
                return jsonify({
                    "success": False,
                    "message": "You do not have permission to access this resource"
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
