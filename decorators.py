import sys
import functools
import jwt
import json
import settings
from logger import log


def decode_jwt(serializer_class):
    """Decode JWT and parse to serializer_class configured."""
    def wrapper(func):
        @functools.wraps(func)
        def decode(*args, **kwargs):
            token_input = None
            try:
                token_input = sys.argv[1]
            except IndexError:
                # Read stdin when token is not passed like args
                token_input = sys.stdin.readline()

            if not token_input:
                log.error('JWT input not received when command was called.')
            else:
                token_data = jwt.decode(
                    token_input,
                    settings.JWT_SECRET,
                    algorithms=['HS512'])

                if token_data['fields']:
                    token_data['fields'] = json.loads(token_data['fields'])

                instance = serializer_class().load(token_data)
                log.info('Decoded JWT')
                return func(instance.data, *args, **kwargs)
        return decode
    return wrapper
