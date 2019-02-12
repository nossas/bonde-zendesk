from marshmallow import fields, validate
from .base import BaseModel, BaseSchema


class UserFieldsSchema(BaseSchema):
    condition = fields.Str()
    neighborhood = fields.Str()
    city = fields.Str()
    state = fields.Str()
    tipo_de_acolhimento = fields.Str()
    # Fields need filled
    address = fields.Str()
    latitude = fields.Str()
    longitude = fields.Str()


class UserFields(BaseModel):
    class Meta:
        schema_class = UserFieldsSchema
        fields = [
            'condition', 'neighborhood', 'city', 'state',
            'tipo_de_acolhimento', 'address', 'latitude', 'longitude'
        ]


class UserSchema(BaseSchema):
    email = fields.Str(required=True, validate=validate.Email())
    name = fields.Str(required=True)
    organization_id = fields.Integer(required=True)
    phone = fields.Str()
    role = fields.Str(
        required=True,
        validate=validate.OneOf(['admin', 'agent', 'end-user']))
    user_fields = fields.Nested(UserFieldsSchema)


class User(BaseModel):
    class Meta:
        schema_class = UserSchema
        fields = [
            'email', 'name', 'organization_id',
            'phone', 'role', 'user_fields'
        ]
