from flask import Flask
from app.extensions import db, migrate, jwt


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models.revoked_token import RevokedToken

    @jwt.token_in_blocklist_loader
    def check_if_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        user_id = jwt_payload["sub"]
        token_type = jwt_payload["type"]
        return RevokedToken.is_revoked(jti, user_id, token_type) 
    
    from app.models.user import User

    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import users_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    
    return app
