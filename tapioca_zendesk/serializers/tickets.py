from marshmallow import fields
from .base_schema import BaseSerializer, BaseSchema


class TicketSchema(BaseSchema):
    subject = fields.Str(required=True)
    description = fields.Str()
    requester_id = fields.Integer(required=True)
    organization_id = fields.Integer(required=True)


class Ticket(BaseSerializer):
    class Meta:
        schema_class = TicketSchema
        fields = ['subject', 'description', 'organization_id', 'requester_id']
