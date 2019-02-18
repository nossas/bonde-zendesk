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


class WidgetSettings(BaseModel):
    class Meta:
        fields = ['email_text', 'email_subject']


class WidgetSettingsSchema(BaseSchema):
    """Schema based on WidgetSettingsSchema"""
    __model__ = WidgetSettings

    email_subject = String()
    email_text = String()


class FormEntry(BaseModel):
    class Meta:
        fields = ['widget_id', 'fields', 'widget_settings']


class FormEntrySchema(BaseSchema):
    """Schema based on FormEntry model."""
    __model__ = FormEntry

    widget_id = Integer(required=True)
    fields = Nested(FormEntryFieldSchema, many=True)
    widget_settings = Nested(WidgetSettingsSchema)
