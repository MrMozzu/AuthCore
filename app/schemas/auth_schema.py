from marshmallow import fields, validate, validates_schema, ValidationError, Schema

class RegisterSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(min=3, max=30)
    )
    username = fields.String(
        required=True, 
        validate=validate.Length(min=3, max=30)
    )
    email = fields.Email(
        required=True
    )
    phone_no = fields.String(
        required=True
    )
    password = fields.String(
        required=True, 
        validate=validate.Length(min=3, max=30)
    )
    confirm_password = fields.String(
        required=True
    )
    
class LoginSchema(Schema):
    email = fields.Email(
        required=True
    )
    password = fields.String(     
        required=True,
        validate=validate.Length(min=3, max=30)
    )

class ForgotPasswordSchema(Schema):
    email = fields.Email(
        required=True
        )

class ResetPasswordSchema(Schema):
    token = fields.String(
        required=True
    )
    new_password = fields.String(
        required=True
    )
    confirm_new_password = fields.String(
        required=True
    )

