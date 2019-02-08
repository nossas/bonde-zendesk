from marshmallow import fields
from .base_schema import BaseSerializer, BaseSchema


class OrganizationSchema(BaseSchema):
    name = fields.Str(required=True)


class Organization(BaseSerializer):

    class Meta:
        schema_class = OrganizationSchema
        fields = ['name']
