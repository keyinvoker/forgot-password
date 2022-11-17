from marshmallow import Schema, fields, ValidationError, validates_schema

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

    class Meta:
        ordered = True

class PasswordResetSchema(Schema):
    password = fields.String(required=True)
    password2 = fields.String(required=True)

    @validates_schema
    def validate_password(self, data):
        if data['password']==data['password2']:
            raise ValidationError('Password does not match!')