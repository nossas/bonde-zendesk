from marshmallow import fields
from .base import BaseSchema, BaseModel


class CustomField(BaseModel):
    class Meta:
        fields = ['id', 'value']


class CustomFieldSchema(BaseSchema):
    __model__ = CustomField

    id = fields.Integer()
    value = fields.Str()


class Comment(BaseModel):
    class Meta:
        fields = ['body']


class CommentSchema(BaseSchema):
    __model__ = Comment

    body = fields.Str()


class Ticket(BaseModel):
    class Meta:
        fields = [
            'id', 'subject', 'requester_id',
            'custom_fields', 'external_id'
        ]


class TicketSchema(BaseSchema):
    __model__ = Ticket

    id = fields.Integer(load_only=True)
    subject = fields.Str(allow_none=True)
    comment = fields.Nested(CommentSchema)
    requester_id = fields.Integer()
    external_id = fields.Str()
    custom_fields = fields.Nested(CustomFieldSchema, many=True, dump_only=True)
