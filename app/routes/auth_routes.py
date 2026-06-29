from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from app.services.auth_service import AuthService 
from app.schemas.auth_schema import RegisterSchema, LoginSchema, ForgotPasswordSchema, ResetPasswordSchema, LogoutSchema
from app.schemas.response_schema import MessageResponseSchema, LoginResponseSchema, RefreshResponseSchema
from flask_smorest import Blueprint
from app.extensions import limiter

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", description="Authentication APIs")

@auth_bp.post("/register")
@auth_bp.arguments(RegisterSchema)
@auth_bp.response(201, MessageResponseSchema)
@limiter.limit("5 per minute") # now we have 5 calls per minute for this route, 
def register(data):
    
    user = AuthService.register(**data)
    
    return jsonify({
        "success": True,
        "message": "User created"
    }), 201
    
    

@auth_bp.post("/login")
@auth_bp.arguments(LoginSchema)
@auth_bp.response(200, LoginResponseSchema)
@limiter.limit("5 per minute")
def login_route(data):

    access_token, refresh_token = AuthService.login(**data)
 
    return jsonify({
            "success": True,
            "message": "login successfull",
            "access_token": access_token,
            "refresh_token": refresh_token
    }), 200
    


@auth_bp.post("/refresh-access-token")  
@auth_bp.doc(security=[{"BearerAuth": []}])
@auth_bp.response(200, RefreshResponseSchema) 
@jwt_required(refresh=True)
@limiter.limit("5 per minute")
def refresh_access_token():
    
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
@limiter.limit("5 per minute")
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
@limiter.limit("5 per minute")
def reset_password(data, token):

    user = AuthService.reset_password(token=token or data.get('token'), new_password=data['new_password'], confirm_new_password=data['confirm_new_password'])
    
    return jsonify({
        "success": True,
        "message": "Password reset successfully"
    }), 200


@auth_bp.post('/refresh')
@auth_bp.doc(security=[{'BearerAuth':[]}])
@auth_bp.response(200, LoginResponseSchema) 
@jwt_required(refresh=True)
@limiter.limit("5 per minute")
def refresh():

    user_id = get_jwt_identity() 
    new_access_token, new_refresh_token = AuthService.refresh_token(user_id)

    return jsonify({
        "success": True,
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "message": "Token refreshed successfully"
    }), 200

@auth_bp.post('/logout')
@auth_bp.doc(security=[{"BearerAuth": []}])
@auth_bp.arguments(LogoutSchema)
@auth_bp.response(200, MessageResponseSchema)
@jwt_required()
@limiter.limit("5 per minute")
def logout(data):
    jwt_payload = get_jwt()
    refresh_token = data.get("refresh_token")
    
    AuthService.logout(jwt_payload, refresh_token)
    
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200

@auth_bp.post('/logout-all')
@auth_bp.doc(security=[{"BearerAuth": []}])
@auth_bp.response(200, MessageResponseSchema)
@jwt_required()
@limiter.limit("5 per minute")
def logout_all_devices():
    jwt_payload = get_jwt()
    
    AuthService.logout_all_devices(jwt_payload)
    
    return jsonify({
        "success": True,
        "message": "Logged out from all devices successfully"
    }), 200


        