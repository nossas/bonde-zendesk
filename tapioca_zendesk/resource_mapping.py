# coding: utf-8

BASE_DOCS_URL = 'https://developer.zendesk.com/rest_api/docs/support'

RESOURCE_MAPPING = {
    'organizations': {
        'resource': 'organizations.json',
        'docs': '{0}/organizations'.format(BASE_DOCS_URL)
    },
    'tickets': {
        'resource': 'tickets.json',
        'docs': '{0}/tickets'.format(BASE_DOCS_URL)
    },
    'user_create_or_update': {
        'resource': 'users/create_or_update.json',
        'docs': '{0}/users#create-or-update-user'.format(BASE_DOCS_URL)
    },
    'user_fields': {
        'resource': 'user_fields.json',
        'docs': '{0}/user_fields'.format(BASE_DOCS_URL)
    },
    'tickets': {
        'resource': 'tickets.json',
        'docs': '{0}/tickets'.format(BASE_DOCS_URL)
    },
}
