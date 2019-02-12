from settings import gmaps
from serializers import GeocodeSchema


def get_geocode(address, many=False):
    geocode_data = gmaps.geocode(address)
    serializer = GeocodeSchema().load(
        geocode_data if many else geocode_data[0],
        many=many
    )
    return serializer.data
