from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from app.services.auth_service import AuthService 
from app.schemas.auth_schema import RegisterSchema, LoginSchema, ForgotPasswordSchema, ResetPasswordSchema
from app.schemas.response_schema import MessageResponseSchema, LoginResponseSchema, RefreshResponseSchema
from flask_smorest import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", description="Authentication APIs")

@auth_bp.post("/register")
@auth_bp.arguments(RegisterSchema)
@auth_bp.response(201, MessageResponseSchema)
def register(data):
    
    user = AuthService.register(**data)
    
    return jsonify({
        "success": True,
        "message": "User created"
    }), 201
    
    

@auth_bp.post("/login")
@auth_bp.arguments(LoginSchema)
@auth_bp.response(200, LoginResponseSchema)
def login_route(data):

    user = AuthService.login(**data)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
            "success": True,
            "message": "login successfull",
            "access_token": access_token,
            "refresh_token": refresh_token
    }), 200
    


@auth_bp.post("/refresh")  
@auth_bp.doc(security=[{"BearerAuth": []}])
@auth_bp.response(200, RefreshResponseSchema) 
@jwt_required(refresh=True)
def refresh_token():
    
    user_id = get_jwt_identity() 
    new_access_token = AuthService.refresh_access_token(user_id)
    
    return jsonify({
        "success": True,
        "access_token": new_access_token,
        "message": "Token refreshed successfully"
    }), 200

    

@auth_bp.post("/forgot-password")
@auth_bp.arguments(ForgotPasswordSchema)
@auth_bp.response(200, MessageResponseSchema)
def forgot_password(data):

    user = AuthService.forgot_password(**data)

    return jsonify({
        "success": True,
        "message": "if email is registered then password reset email sent successfully"
    }), 200 


# reset password 

@auth_bp.post("/reset-password/<string:token>")
@auth_bp.arguments(ResetPasswordSchema)
@auth_bp.response(200, MessageResponseSchema)
def reset_password(data, token):

    user = AuthService.reset_password(token=token or data.get('token'), new_password=data['new_password'], confirm_new_password=data['confirm_new_password'])
    
    return jsonify({
        "success": True,
        "message": "Password reset successfully"
    }), 200