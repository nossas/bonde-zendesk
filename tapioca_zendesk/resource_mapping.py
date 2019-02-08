# coding: utf-8

BASE_DOCS_URL = 'https://developer.zendesk.com/rest_api/docs/support'

RESOURCE_MAPPING = {
    'organizations': {
        'resource': 'organizations/autocomplete.json',
        'docs': '{0}/organizations#autocomplete-organizations'.format(
            BASE_DOCS_URL)
    },
    'users': {
        'resource': 'users.json',
        'docs': '{0}/users'.format(BASE_DOCS_URL)
    },
    'tickets': {
        'resource': 'tickets.json',
        'docs': '{0}/tickets'.format(BASE_DOCS_URL)
    },
}
