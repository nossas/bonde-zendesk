from marshmallow import Schema, ValidationError


class BaseSchema(Schema):
    class Meta:
        strict = True


class ModelFactory(type):
    def __new__(meta, cls, base, dct):
        self = super().__new__(meta, cls, base, dct)
        if cls != 'BaseModel':
            self._meta = self.Meta
        return self


class BaseModel(metaclass=ModelFactory):
    def __init__(self, many=False, **kwargs):
        # Add fields passed on constructor
        values = kwargs.copy()
        for field in self._meta.fields:
            setattr(self, field, values.get(field))

        # Load schema to run validate fields schema
        self._meta.schema_class(many=many).load(values)
