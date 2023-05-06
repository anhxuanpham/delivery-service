# File controller.py 
# Created at 24/03/2023
# Author Khanh

import bcrypt
from flask import g, request
from schemas.auth import FormToken, FormUserLoginSchema, UserAuthSchema, FormUserRegisterSchema, FormRefreshToken
from src.services.user import UserService
import vibe_library.decorators as deco
from vibe_library.exceptions import RequiredAuth

from vibe_library.handlerespon import make_response

@deco.handle_response()
@deco.load_data(FormUserLoginSchema)
def login_cl() -> dict:
    """
        - Control the login action of user  
    """
    _user_data = g.data 

    # check_password = bcrypt.hashpw('123456'.encode('utf8'), bcrypt.gensalt(10)).decode('utf-8')
    # print('---check_password---', check_password)

    result = UserService.login(
        phone = _user_data.get('phone'),
        password = _user_data.get('password'),
    )
    return UserAuthSchema.load_response(result)

@deco.handle_response()
@deco.load_data(FormToken)
def logout_cl() -> dict:

    _token = g.data 
    print('-----token------',_token)
    result = ''
    return 'hello'

@deco.handle_response()
@deco.load_data(FormRefreshToken)
def refresh_token_cl():
    _token_info, _request_token = deco.get_token()
    if not _token_info:
        raise RequiredAuth
    
    _data = g.data
    _refresh_token = _data.get('refresh_token')
    result = UserService.refresh(refresh_token=_refresh_token, request_token=_request_token, obj_type='user_account')
    return result

@deco.handle_response()
@deco.load_data(FormUserRegisterSchema)
def register_cl():
    """ 
        - Control the register action of user
    """
    _data = g.data
    result = UserService.register(
        name=_data.get('name'),
        phone=_data.get('phone'),
        password=_data.get('password'),
        store_id=_data.get('store_id'),
        email=_data.get('email'),
        address=_data.get('address'),
        permission=_data.get('permission'),
    )
    return result