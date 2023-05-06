# File decorators.py 
# Created at 25/03/2023
# Author Khanh

import hashlib
import hmac
import json
from functools import wraps

import sentry_sdk
from marshmallow import ValidationError

from .enums import ReqMimetype

from .exceptions import MissingData, RequiredAuth, request_exception
from flask import request, jsonify, g
import jwt
import traceback

from .handlerespon import make_response
import bson.json_util as bson_json
from .extensions import redis_single


def gen_auth_key(obj_type: str, payload: dict):
    if obj_type == 'user_account':
        return f"tokens:user_account:{payload.get('phone')}"

CACHE_TIMEOUT_FACTOR = 1

def handle_response(schema=None, mimetype=None, caching=False, timeout=604800, default=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            @request_exception(default=default, mimetype=mimetype)
            def run_controller():
                if mimetype and mimetype == ReqMimetype.STREAM:
                    return f(*args, **kwargs)

                # @cache_request(
                #     keep_timeout=timeout,
                #     key_prefix=request.path
                # )
                def run_with_cache():
                    return f(*args, **kwargs)

                if caching:
                    data = run_with_cache()
                else:
                    data = f(*args, **kwargs)
                if isinstance(data, tuple):
                    # data, msg
                    return make_response(data=data[0], msg=data[1])
                # data: dict
                if schema:
                    data = schema().load(data)
                return make_response(data)

            if mimetype and mimetype == ReqMimetype.STREAM:
                return run_controller()

            return jsonify(run_controller()), 200

        return wrapper

    return decorator


def load_data(BaseSchema):
    """
    Decorator to load data from request
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.method == 'GET':
                request_data = request.args.to_dict()
            else:
                request_data = request.get_json()
            schema = BaseSchema()
            try:
                result = schema.load(request_data)
                g.data = result
            except ValidationError as err:
                errors = err.messages
                msg = ''
                if isinstance(errors, str):
                    msg = errors
                if isinstance(errors, list) and isinstance(errors[0], dict):
                    field, msg = errors[0].items()[0]
                if isinstance(errors, dict) and len(errors.items()) > 0:
                    field, msg = list(errors.items())[0]
                    if isinstance(msg, list):
                        msg = msg[0]
                if not msg:
                    msg = str(errors)
                raise MissingData(message=msg, errors=errors)
            except:
                raise
            return f(*args, **kwargs)

        return wrapper

    return decorator

def get_token_info(token):
    try:
        return jwt.decode(token, algorithms='RS256', options={"verify_signature": False})
    except:
        return False

def get_token():
    _request_token = request.headers.get('Authorization')
    if not _request_token or 'Bearer ' not in _request_token:
        _request_token = request.args.get('access_token', type=str)

        if not _request_token:
            return None, None
    else:
        _request_tokens = _request_token.split(' ')
        if len(_request_tokens) < 1:
            return None, None
        _request_token = _request_tokens[1]

        # Get user token on Redis user info
        _info = get_token_info(_request_token)
        if not isinstance(_info, dict):
            return None, None
        if not _info.get('payload'):
            return None, None
        
        return _info.get('payload'), _request_token


def verify_token_request(obj_type: str):
    """
        - The function that verifies token
    """
    _token_info, _request_token = get_token()

    if not _token_info:
        return {}
    
    _token_existed = redis_single.get(gen_auth_key(obj_type=obj_type, payload=_token_info))
    if _token_existed:
        _token_existed = _token_existed.decode()

    if _token_existed and _token_existed == _request_token:
        return _token_info

    return False


def gen_decorator(key:str, obj_type: str, is_required: bool = True):
    def decorator(f):
        @wraps(f)

        def wrapper(*args, **kwargs):

            if not request:
                
                decorator_kwargs = {**kwargs, key: {}}
                
                return f(*args, decorator_kwargs)
            
            auth_info = verify_token_request(obj_type)

            if not auth_info:
                raise RequiredAuth
            
            if auth_info == {}:
                if is_required:
                    raise RequiredAuth
                else:
                    auth_info = {}

            decorator_kwargs = {**kwargs, key: auth_info}
            
            return f(*args, **decorator_kwargs)
        
        return wrapper

    return decorator


def auth_user():
    """
        - Decorator to check and get user info from user token, Return
    """
    return gen_decorator(key='user', obj_type='user_account', is_required=False)

