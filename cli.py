#!/usr/bin/python
"""
CLI for manipulate Zendesk Rest API
"""
import os
from tapioca_zendesk import Zendesk

ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN')
ZENDESK_API_USER = os.getenv('ZENDESK_API_USER')

if not ZENDESK_API_TOKEN or not ZENDESK_API_USER:
    warning = 'ZENDESK_API_USER not environment.' if not ZENDESK_API_TOKEN \
        else 'ZENDESK_API_TOKEN not environment.'
    raise Exception(warning)


api_rest = Zendesk(user=ZENDESK_API_USER, password=ZENDESK_API_TOKEN)


def filter_organizations(**kwargs):
    resp = api_rest.organizations().get(params=kwargs)
    return resp.organizations


if __name__ == '__main__':
    print(filter_organizations(name='terapeuta'))
