from marshmallow.fields import String, Integer, Nested
from .base import BaseSchema, BaseModel


class FormEntryField(BaseModel):
    class Meta:
        fields = ['uid', 'kind', 'label', 'value']


class FormEntryFieldSchema(BaseSchema):
    """Schema based on FormEntryField model."""
    __model__ = FormEntryField

    uid = String(required=True)
    kind = String(required=True)
    label = String(required=True)
    value = String()


class FormEntry(BaseModel):
    class Meta:
        fields = ['id', 'widget_id', 'fields', 'created_at']


class FormEntrySchema(BaseSchema):
    """Schema based on FormEntry model."""
    __model__ = FormEntry

    id = Integer(load_only=True)
    widget_id = Integer(required=True)
    fields = Nested(FormEntryFieldSchema, many=True)
    created_at = String(required=True)
