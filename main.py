#!/usr/bin/env python
# coding: utf-8
import sys
import jwt
import settings
import cli
from tapioca_zendesk.serializers import User

RESOURCE_SERIALIZERS = {
    'create_user': User
}


if __name__ == '__main__':
    token_input = sys.argv[1]
    args = jwt.decode(
        token_input,
        settings.JWT_SECRET,
        algorithms=['HS256'])

    command = args.get('command')
    payload = args.get('payload')

    Serializer = RESOURCE_SERIALIZERS.get(command)
    obj = Serializer(**payload)

    # Execute a command on CLI arguments is a serializable object.
    getattr(cli, command)(obj)
