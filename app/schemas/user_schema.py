from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    phone_no = fields.String(required=True)
    is_verified = fields.Boolean(required=True)
    role = fields.String(dump_only=True)
    
class UpdateUserSchema(Schema):
    email = fields.Email(required=True)
    phone_no = fields.String(required=True)

class UserResponseSchema(Schema):
    name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    phone_no = fields.String(required=True)
    is_verified = fields.Boolean(required=True)
    role = fields.String(required=True)

class ChangePasswordSchema(Schema):
    old_password = fields.String(
        required=True,
        validate=validate.Length(min=3, max=30)
    )
    new_password = fields.String(
        required=True,
        validate=validate.Length(min=3, max=30)
    )
    confirm_new_password = fields.String(
        required=True,
        validate=validate.Length(min=3, max=30)
    )

class UpdateRoleSchema(Schema):
    role = fields.String(
        required=True,
        validate=validate.OneOf(["user", "moderator", "admin"])
    )


