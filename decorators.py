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
            log.info('stdin')
            log.info(sys.stdin.readline())
            token_input = None
            try:
                token_input = sys.argv[1]
            except IndexError:
                log.info(
                    'JWT input wasn\'t received like args. ' +
                    'Reading stdin to search token input'
                )
                token_input = sys.stdin.readline()

            if not token_input:
                log.error('JWT input not received when command was called.')
            else:
                json = jwt.decode(
                    token_input,
                    settings.JWT_SECRET,
                    algorithms=['HS512'])
                obj = serializer_class(**json)
                log.info('Decoded JWT')
                return func(obj, *args, **kwargs)
        return decode
    return wrapper
