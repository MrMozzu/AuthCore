from flask import Flask
from app.extensions import db, migrate, jwt, mail, api 
from app.errors.handlers import register_error_handlers


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    app.config["API_TITLE"] = "Authentication API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_COMPONENTS"] = {
    "securitySchemes": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
}

    app.config["OPENAPI_URL_PREFIX"] = "/"

    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"

    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    api.init_app(app)
    limiter.init_app(app)

    from app.models.revoked_token import RevokedToken
    from app.models.password_reset_token import PasswordResetToken
    from app.models.refresh_token import RefreshToken
    from app.models.email_verification_model import EmailVerification

    @jwt.token_in_blocklist_loader
    def check_if_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        user_id = jwt_payload["sub"]
        token_type = jwt_payload["type"]
        return RevokedToken.is_revoked(jti, user_id, token_type) 
    
    from app.models.user import User

    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import users_bp
    
    api.register_blueprint(auth_bp)
    api.register_blueprint(users_bp)
    register_error_handlers(app)
    
    return app
