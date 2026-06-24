class APIException(Exception):
    status = 400
    message = "API error"

    def __init__(self, message=None):
        self.message = message

        if message:
            self.message = message
        super().__init__(self.message)



class ConflictError(APIException):
    status = 409
    message = "Resource already exists" 

class EmailNotVerifiedError(APIException):  
    status = 401
    message = "Email not verified"

class InvalidCredentialsError(APIException):
    status = 401
    message = "Invalid Credentials"

class InvalidTokenError(APIException):
    status = 401
    message = "Invalid Token"

class ExpiredTokenError(APIException):
    status = 401
    message = "Token is expired"

class UserNotFoundError(APIException):
    status = 404
    message = "User not found"

class ResourceNotFoundError(APIException):
    status = 404
    message = "Resource not found"

class Unauthorized(APIException):
    status = 401
    message = "Unauthorized"
 

