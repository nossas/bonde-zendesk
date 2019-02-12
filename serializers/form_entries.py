from marshmallow import fields
from .base import BaseSchema, BaseModel


class FormEntryField(BaseModel):
    class Meta:
        fields = ['uid', 'kind', 'label', 'value']


class FormEntryFieldSchema(BaseSchema):
    """Schema based on FormEntryField model."""
    __model__ = FormEntryField

    uid = fields.String(required=True)
    kind = fields.String(required=True)
    label = fields.String(required=True)
    value = fields.String()


class FormEntry(BaseModel):
    class Meta:
        fields = ['widget_id', 'fields']


class FormEntrySchema(BaseSchema):
    """Schema based on FormEntry model."""
    __model__ = FormEntry

    widget_id = fields.Integer(required=True)
    fields = fields.Nested(FormEntryFieldSchema, many=True)
