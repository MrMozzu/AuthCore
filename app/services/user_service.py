from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def get_current_user(user_id):

        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError("User does not exists")
        return user


    @staticmethod
    def update_user(user_id, email, phone_no):
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        if email:
            user.email = email

        if phone_no:
            user.phone_no = phone_no
        
        try:
            updated_user = UserRepository.update(user)
            return updated_user

        except:
            raise Exception("Error while updating user")

    
    @staticmethod
    def update_password(user_id, old_password, new_password):
        user = UserRepository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        if not user.check_password(old_password):
            raise ValueError("Incorrect old password")

        user.set_password(new_password)

        try:
            updated_user = UserRepository.update(user)
            return updated_user
        
        except:
            raise Exception("Error while updating passowrd")

    



    