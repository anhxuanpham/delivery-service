# File jwt.py 
# Created at 26/03/2023
# Author Khanh

from datetime import datetime, timedelta
from vibe_library.exceptions import handle_exception
from src.config import DefaultConfig
import jwt
import vibe_library.decorators as deco
from vibe_library.extensions import redis_single

with open('keys/token_key.pem') as f:
    TOKEN_KEY = f.read()

@handle_exception()
def gen_token(obj_type: str, payload: dict) -> str:
    """
        - The function that generates a token based on user
        :param obj_type
        :param payload
        :return str
    """
    token_payload = {
        # info token
        'payload': payload,
        'iat': datetime.utcnow(), #init time
        'exp': datetime.utcnow() + timedelta(seconds=DefaultConfig.TOKEN_EXP_TIME),
    }
    encoded_token = jwt.encode(token_payload, TOKEN_KEY, algorithm='RS256')
    """
        - Whent saving replace new token => token old cannot be use
    """
    _key = deco.gen_auth_key(obj_type=obj_type, payload=payload)
    redis_single.setex(_key, DefaultConfig.TOKEN_EXP_TIME, encoded_token)
    return encoded_token

@handle_exception()
def gen_refresh_token(token: str, obj_type: str = 'users') -> str:
    """
        - The function that generates a refresh token based on current token
        :param token
        :param obj_type
        :return str
    """
    token_payload = {
        'payload': {
            'token': token
        },
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(
            seconds=DefaultConfig.TOKEN_EXP_TIME + DefaultConfig.REFRESH_TOKEN_EXP_TIME),
    }
    encoded_refresh_token = jwt.encode(token_payload, TOKEN_KEY, algorithm='RS256')
    """
        - Saving refresh token. After use, The system must delete it;
    """
    redis_single.setex(f'tokens:refresh_tokens:{obj_type}:{encoded_refresh_token}',
                       DefaultConfig.TOKEN_EXP_TIME + DefaultConfig.REFRESH_TOKEN_EXP_TIME, token)

    return encoded_refresh_token

@handle_exception()
def gen_user_token(user_info: dict) -> str:
    """
        - The function that generates a token based on user account
        :param user_info
        :return str
    """
    return gen_token(obj_type='user_account', payload={
        'phone': user_info.get('phone'),
        'email': user_info.get('email'),
        'store_id': user_info.get('store_id'),
        'name': user_info.get('name')
    })