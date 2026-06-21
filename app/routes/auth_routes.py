from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.services.auth_service import AuthService 
from app.schemas.auth_schema import RegisterSchema, LoginSchema, ForgotPasswordSchema, ResetPasswordSchema


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():

    data = RegisterSchema().load(request.get_json())
    
    user = AuthService.register(**data)
    
    return jsonify({
        "message": "User created"
    }), 201
    
    

@auth_bp.post("/login")
def login_route():

    data = LoginSchema().load(request.get_json())

    user = AuthService.login(**data)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
            "message": "login successfull",
            "access_token": access_token,
            "refresh_token": refresh_token
    }), 200
    


@auth_bp.post("/refresh")  
@jwt_required(refresh=True)
def refresh_token():
    
    user_id = get_jwt_identity()
    new_access_token = AuthService.refresh_access_token(user_id)
    
    return jsonify({
        "access_token": new_access_token,
        "message": "Token refreshed successfully"
    }), 200

    

@auth_bp.post("/forgot-password")
def forgot_password():

    data = ForgotPasswordSchema().load(request.get_json())
    user = AuthService.forgot_password(**data)

    return jsonify({
        "message": "if email is registered then password reset email sent successfully"
    }), 200 


# reset password 

@auth_bp.post("/reset-password/<string:token>")
def reset_password(token):

    data = ResetPasswordSchema().load(request.get_json())

    user = AuthService.reset_password(**data)
    
    return jsonify({
        "message": "Password reset successfully"
    }), 200