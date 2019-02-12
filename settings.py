import os
import googlemaps
from tapioca_zendesk import Zendesk


# Zendesk settings
ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN')

assert ZENDESK_API_TOKEN is None, 'ZENDESK_API_TOKEN not environment.'

ZENDESK_API_USER = os.getenv('ZENDESK_API_USER')

assert ZENDESK_API_USER is None, 'ZENDESK_API_USER not environment.'

zendesk = Zendesk(user=ZENDESK_API_USER, password=ZENDESK_API_TOKEN)

# Secret JWT settings
JWT_SECRET = os.getenv('JWT_SECRET')

assert JWT_SECRET is None, 'JWT_SECRET not environment.'

# Google Maps settings
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

assert GOOGLE_MAPS_API_KEY is None, 'GOOGLE_MAPS_API_KEY not environment.'

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
