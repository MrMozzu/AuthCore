from marshmallow import Schema, fields, validate

class MessageResponseSchema(Schema):
    message = fields.String(
        required=True
    )
    success = fields.Boolean(
        required=True
    )
    

class LoginResponseSchema(Schema):
    success = fields.Boolean(
        required=True
    )
    
    message = fields.String(
        required=True
    )
    
    access_token = fields.String(
        required=True
    )
    
    refresh_token = fields.String(
        required=True
    )


class TokenResponseSchema(Schema):
    success = fields.Boolean(
        required=True
    )
    access_token = fields.String(
        required=True
    )


class UserResponseSchema(Schema):
    success = fields.Boolean(
        required=True
    )
    
    message = fields.String(
        required=True
    )
    
    user = fields.Dict(
        required=True
    )

class RefreshResponseSchema(Schema):
    success = fields.Boolean(
        required=True
    )
    
    message = fields.String(
        required=True
    )
    
    access_token = fields.String(
        required=True
    )