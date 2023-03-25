# File controller.py 
# Created at 24/03/2023
# Author Khanh


from flask import g, request
from schemas.auth import FormUserLoginSchema
from src.services.user import UserService
import vibe_library.decorators as deco


@deco.handle_response()
@deco.load_data(FormUserLoginSchema)
def login_cl():
    """
        - Control the login action of user  
    """
    _user_data = g.data 
    print('----_user_data----', _user_data)
    print('----function login cl has work-----')
    result = UserService.login(
        phone = _user_data.get('phone'),
        password = _user_data.get('password')
    )
    return 'hello'