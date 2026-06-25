from app.extensions import db
from app.models.user import User


class UserRepository:
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_phone_no(phone_no):
        return User.query.filter_by(phone_no=phone_no).first()

    @staticmethod
    def create(user):
        try:
            db.session.add(user)
            db.session.commit()
        
        except:
            db.session.rollback()
            raise Exception('Error while saving user')
        
        return user

    @staticmethod
    def update(user):

        if not user:
            raise Exception("User not found")
        
        try:
            db.session.add(user)
            db.session.commit()
            return user

        except:
            db.session.rollback()
            raise Exception("Error while updating user")



    