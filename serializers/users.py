from marshmallow import fields, validate
from .base import BaseSchema, BaseModel


class UserFields(BaseModel):
    class Meta:
        fields = [
            'condition', 'neighborhood', 'city', 'state',
            'tipo_de_acolhimento', 'address', 'latitude',
            'longitude'
        ]


class UserFieldsSchema(BaseSchema):
    __model__ = UserFields

    # Fields need filled
    condition = fields.Str(allow_none=True)
    neighborhood = fields.Str()
    city = fields.Str()
    state = fields.Str()
    tipo_de_acolhimento = fields.Str()
    address = fields.Str()
    latitude = fields.Decimal(allow_none=True)
    longitude = fields.Decimal(allow_none=True)


class User(BaseModel):
    class Meta:
        fields = [
            'id', 'email', 'external_id', 'name',
            'organization_id', 'phone', 'role',
            'user_fields'
        ]


class UserSchema(BaseSchema):
    __model__ = User

    id = fields.Integer(load_only=True)
    email = fields.Str(required=True, validate=validate.Email())
    external_id = fields.Str(allow_none=True)
    name = fields.Str(required=True)
    organization_id = fields.Integer(required=True)
    phone = fields.Str(allow_none=True)
    role = fields.Str(
        required=True,
        validate=validate.OneOf(['admin', 'agent', 'end-user']))
    user_fields = fields.Nested(UserFieldsSchema)
