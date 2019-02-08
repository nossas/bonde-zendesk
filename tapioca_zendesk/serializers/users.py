from marshmallow import fields, validate
from .base_schema import BaseSerializer, BaseSchema


class UserFieldsSchema(BaseSchema):
    city = fields.Str()


class UserFields(BaseSerializer):
    class Meta:
        schema_class = UserFieldsSchema
        fields = ['city']


class UserSchema(BaseSchema):
    email = fields.Str(required=True, validate=validate.Email())
    name = fields.Str(required=True)
    organization_id = fields.Integer(required=True)
    phone = fields.Str()
    role = fields.Str(
        required=True,
        validate=validate.OneOf(['admin', 'agent', 'end-user']))
    user_fields = fields.Nested(UserFieldsSchema)


class User(BaseSerializer):
    class Meta:
        schema_class = UserSchema
        fields = [
            'email', 'name', 'organization_id',
            'phone', 'role', 'city', 'user_fields'
        ]
