from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    phone_no = fields.String(required=True)
    
class UpdateUserSchema(Schema):
    email = fields.Email(required=True)
    phone_no = fields.String(required=True)

class UserResponseSchema(Schema):
    name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    phone_no = fields.String(required=True)
    is_verified = fields.Boolean(required=True)



