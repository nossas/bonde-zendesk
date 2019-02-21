from settings import gmaps
from serializers import GeocodeSchema


class AddressNotFound(Exception):
    pass


def get_geocode(address, many=False):
    geocode_data = gmaps.geocode(address)

    if len(geocode_data) == 0:
        raise AddressNotFound('{0} not found.'.format(address))

    serializer = GeocodeSchema().load(
        geocode_data if many else geocode_data[0],
        many=many
    )
    return serializer.data
