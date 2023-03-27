# File controller.py 
# Created at 24/03/2023
# Author Khanh

import bcrypt
from flask import g, request
from schemas.auth import FormUserLoginSchema, UserAuthSchema
from src.services.user import UserService
import vibe_library.decorators as deco

from vibe_library.handlerespon import make_response

@deco.handle_response()
@deco.load_data(FormUserLoginSchema)
def login_cl():
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
    # return make_response(
    #     data=result
    # )
    return UserAuthSchema.load_response(result)
