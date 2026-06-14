from datetime import datetime
from app.extensions import db 
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.mixins.timestampmixin import TimeStampMixin


class User(TimeStampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone_no = db.Column(db.Integer, nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(300), unique=True, nullable=False) 
    password_hash = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # it checks the hashed password, doesn't check the original password 
        return check_password_hash(self.password_hash, password)

        