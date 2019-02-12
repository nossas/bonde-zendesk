import json
from marshmallow import fields
from .base import BaseModel, BaseSchema


class FormEntryFields(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''
        return json.loads(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return json.dumps(value)


class FormEntryFieldSchema(BaseSchema):
    """Schema based on FormEntryField model."""
    uid = fields.String(required=True)
    kind = fields.String(required=True)
    label = fields.String(required=True)
    value = fields.String()


class FormEntrySchema(BaseSchema):
    """Schema based on FormEntry model."""
    widget_id = fields.Integer(required=True)
    fields = FormEntryFields()


class FormEntryField(BaseModel):
    """FormEntryField model."""
    class Meta:
        schema_class = FormEntryFieldSchema
        fields = ['uid', 'kind', 'label', 'value']


class FormEntry(BaseModel):
    """FormEntry model."""
    class Meta:
        schema_class = FormEntrySchema
        fields = ['widget_id', 'fields']

    @property
    def xfields(self):
        return [FormEntryField(**fields) for fields in json.loads(self.fields)]

    @xfields.setter
    def xfields(self, value):
        self.fields = json.dumps(value)
