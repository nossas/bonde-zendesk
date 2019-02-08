#!/usr/bin/python
"""
CLI for manipulate Zendesk Rest API
"""
from settings import api


def create_user(user):
    """Create User on Zendesk API"""
    try:
        resp = api.users().post(data=dict(user=user.as_json()))
        # TODO: what to do from here?
        return resp.user
    except Exception as err:
        print('CLI create_user raised.', err)
        pass
