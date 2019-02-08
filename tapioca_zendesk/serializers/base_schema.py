from marshmallow import Schema, ValidationError


class BaseSchema(Schema):
    class Meta:
        strict = True


class BaseMeta(type):
    def __new__(meta, cls, base, dct):
        self = super().__new__(meta, cls, base, dct)
        if cls != 'BaseSerializer':
            self._meta = self.Meta
        return self


class BaseSerializer(metaclass=BaseMeta):
    def __init__(self, many=False, **kwargs):
        # Add fields passed on constructor
        values = kwargs.copy()
        for field in self._meta.fields:
            if hasattr(values.get(field), 'as_json'):
                values.update({field: values.get(field).as_json()})
            setattr(self, field, values.get(field))
        # Load schema to run validate fields schema
        self._meta.schema_class(many=many).load(values)

    def as_json(self):
        schema = self._meta.schema_class()
        data, errors = schema.dump(self)
        # TODO: Validate
        return data
