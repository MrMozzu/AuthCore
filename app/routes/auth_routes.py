from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.services.auth_service import AuthService 
from app.exceptions import ConflictError


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data provided"
        }), 400

    name = data.get("name")

    if not name:
        raise ValueError("Name is required")

    username = data.get("username")
    
    if not username:
        raise ValueError("Username is required")

    email = data.get("email")

    if not email:
        raise ValueError("Email is required")

    phone_no = data.get("phone_no")

    if not phone_no:
        raise ValueError("Phone number is required")

    password = data.get("password")

    if not password:
        raise ValueError("Password is required")
 
    try:
        AuthService.register(name, username, email, phone_no, password)
        return jsonify({"message": "User created"}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except ConflictError as e:
        return jsonify({"error": str(e)}), 409

    

@auth_bp.post("/login")
def login_route():

    data = request.get_json()


    if not data:
        return jsonify({
            "error": "Please provide your details"
        }), 400

    email = data.get("email")
    if not email:
        raise ValueError("Please provide your email")
    
    password = data.get("password")
    if not password:
        raise ValueError("Password is required")

    try:
        user = AuthService.login(email, password)
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