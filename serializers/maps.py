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
        fields = ['formatted_address', 'geometry']


class GeocodeSchema(BaseSchema):
    __model__ = Geocode

    formatted_address = fields.Str(required=True)
    geometry = fields.Nested(GeometrySchema)
