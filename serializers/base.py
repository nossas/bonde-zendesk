from marshmallow import Schema, post_load


class BaseSchema(Schema):
    class Meta:
        strict = True

    __model__ = object

    @post_load
    def make_object(self, data):
        return self.__model__(**data)


class ModelFactory(type):
    def __new__(meta, cls, base, dct):
        self = super().__new__(meta, cls, base, dct)
        if cls != 'BaseModel':
            self._meta = self.Meta
        return self


class BaseModel(metaclass=ModelFactory):
    def __init__(self, **kwargs):
        # Add fields passed on constructor
        values = kwargs.copy()
        for field in self._meta.fields:
            setattr(self, field, values.get(field))
