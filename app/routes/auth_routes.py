from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.services.auth_service import AuthService 
from app.exceptions import ConflictError
from app.schemas.auth_schema import RegisterSchema, LoginSchema, ForgotPasswordSchema, ResetPasswordSchema


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():

    data = RegisterSchema().load(request.get_json())
    
    try:
        user = AuthService.register(**data)
        return jsonify({"message": "User created", "user": UserResponseSchema.dump(user)}), 201

    except ValueError as e: # we can remove the 
        return jsonify({"error": str(e)}), 400

    except ConflictError as e:
        return jsonify({"error": str(e)}), 409

    

@auth_bp.post("/login")
def login_route():

    data = LoginSchema().load(request.get_json())

    try:
        user = AuthService.login(**data)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify({
            "message": "login successfull",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@auth_bp.post("/refresh")  
@jwt_required(refresh=True)
def refresh_token():
    try:

        user_id = get_jwt_identity()
        new_access_token = AuthService.refresh_access_token(user_id)

    except ValueError as e:
        return jsonify({"error": str(e)}), 404 

    return jsonify({
        "access_token": new_access_token,
        "message": "Token refreshed successfully"
    }), 200

    

@auth_bp.post("/forgot-password")
def forgot_password():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    email = data.get("email")
    if not email:
        return jsonify({"error": "email is required"}), 400 

    try:
        AuthService.forgot_password(email)
        return jsonify({"message": "if email is registered then password reset email sent successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# reset password 

@auth_bp.post("/reset-password/<string:token>")
def reset_password(token):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    new_password = data.get("new_password")
    if not new_password:
        return jsonify({"error": "new_password is required"}), 400 

    user_id = get_jwt_identity()

    try:
        AuthService.reset_password(token, new_password)
        return jsonify({"message": "Password reset successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500