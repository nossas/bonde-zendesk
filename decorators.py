import sys
import functools
import jwt
import settings
from logger import log


def decode_jwt(serializer_class):
    """Decode JWT and parse to serializer_class configured."""
    def wrapper(func):
        @functools.wraps(func)
        def decode(*args, **kwargs):
            token_input = sys.argv[1]
            json = jwt.decode(
                token_input,
                settings.JWT_SECRET,
                algorithms=['HS512'])
            obj = serializer_class(**json)
            log.info('Decoded JWT')
            return func(obj, *args, **kwargs)
        return decode
    return wrapper
