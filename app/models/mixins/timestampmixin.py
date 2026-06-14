from app.extensions import db 
from datetime import datetime 


class TimeStampMixin(db.Model):

    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=False)

