import os
import googlemaps
from tapioca_zendesk import Zendesk

DEBUG = bool(int(os.environ.get('DEBUG', 1)))

# Zendesk settings
ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN')

assert ZENDESK_API_TOKEN is not None, 'ZENDESK_API_TOKEN not environment.'

ZENDESK_API_USER = os.getenv('ZENDESK_API_USER')

assert ZENDESK_API_USER is not None, 'ZENDESK_API_USER not environment.'

zendesk = Zendesk(user=ZENDESK_API_USER, password=ZENDESK_API_TOKEN)

# Secret JWT settings
JWT_SECRET = os.getenv('JWT_SECRET')

assert JWT_SECRET is not None, 'JWT_SECRET not environment.'

# Google Maps settings
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

assert GOOGLE_MAPS_API_KEY is not None, 'GOOGLE_MAPS_API_KEY not environment.'

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Sendgrid settings
SENDGRID_SEND_EMAIL = os.environ.get('SENDGRID_SEND_EMAIL')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
if not DEBUG:
    assert SENDGRID_SEND_EMAIL is not None, \
        'SENDGRID_SEND_EMAIL not environment'
    assert SENDGRID_API_KEY is not None, 'SENDGRID_API_KEY not environment.'
