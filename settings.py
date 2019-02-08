import os
from tapioca_zendesk import Zendesk


ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN')

if not ZENDESK_API_TOKEN:
    raise Exception('ZENDESK_API_TOKEN not environment.')

ZENDESK_API_USER = os.getenv('ZENDESK_API_USER')

if not ZENDESK_API_USER:
    raise Exception('ZENDESK_API_USER not environment.')

# Secret JWT
JWT_SECRET = os.getenv('JWT_SECRET')

if not JWT_SECRET:
    raise Exception('JWT_SECRET not environment.')


api = Zendesk(user=ZENDESK_API_USER, password=ZENDESK_API_TOKEN)
