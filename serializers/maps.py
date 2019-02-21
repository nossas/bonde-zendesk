from marshmallow import fields
from .base import BaseSchema, BaseModel


class Location(BaseModel):
    class Meta:
        fields = ['lat', 'lng']


class LocationSchema(BaseSchema):
    __model__ = Location

    lat = fields.Decimal(required=True)
    lng = fields.Decimal(required=True)


class Geometry(BaseModel):
    class Meta:
        fields = ['location']


class GeometrySchema(BaseSchema):
    __model__ = Geometry

    location = fields.Nested(LocationSchema)


class Geocode(BaseModel):
    class Meta:
        fields = ['formatted_address', 'geometry', 'state']


class StateField(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        # Find state level field to get a short_name
        try:
            level = 'administrative_area_level_1'
            state = list(filter(lambda x: level in x['types'], value))[0]
            return state['short_name']
        except IndexError:
            level = 'locality'
            state = list(filter(lambda x: level in x['types'], value))[0]
            if state['short_name'] == 'Florianópolis':
                return 'sc'
            # Treatment only for Florianopolis island
            raise IndexError


class GeocodeSchema(BaseSchema):
    __model__ = Geocode

    formatted_address = fields.Str(required=True)
    geometry = fields.Nested(GeometrySchema)
    address_components = StateField(attribute='state')
