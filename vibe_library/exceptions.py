import traceback
from functools import wraps

import sentry_sdk
from flask import Response
# File exceptions.py 
# Created at 25/03/2023
# Author Khanh

from .enums import ReqMimetype
from .schema import Message
from .handlerespon import make_response
from marshmallow import ValidationError

class RequestException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = {}

    pass

class MissingData(RequestException):
    def __init__(self, message='Missing data', errors={}, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='E_DATA_INVALID',
            status=0,
            msg=message,
            errors=errors
        )

    pass

def request_exception(default: dict = {}, mimetype=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except RequestException as e:
                if mimetype and mimetype == ReqMimetype.STREAM:
                    return Response(
                        str(Message(data=e.response, type='error')),
                        mimetype='text/event-stream',
                    )
                return e.response
            except ValidationError as err:
                errors = err.messages

                resp = make_response(
                    status=0,
                    msg='error load schema of response',
                    error_code='E_SCHEMA_RES',
                    errors=errors
                )
                if mimetype and mimetype == ReqMimetype.STREAM:
                    return Response(
                        str(Message(data=resp, type='error')),
                        mimetype='text/event-stream',
                    )
                return resp
            except:
                sentry_sdk.capture_exception()
                traceback.print_exc()
                if default:
                    return make_response(data=default)
                resp = make_response(
                    status=0,
                    msg='unknown error',
                    error_code='E_SERVER'
                )
                if mimetype and mimetype == ReqMimetype.STREAM:
                    return Response(
                        str(Message(data=resp, type='error')),
                        mimetype='text/event-stream',
                    )
                return resp

        return wrapper

    return decorator

def handle_exception(default=None, tracking=True, is_raise=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                if tracking:
                    sentry_sdk.capture_exception()
                    traceback.print_exc()
                if is_raise:
                    raise
                return default

        return wrapper

    return decorator
