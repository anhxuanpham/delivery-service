# File user.py 
# Created at 24/03/2023
# Author Khanh

from vibe_library.decorators import get_token_info
from src.enums.user import UserAccountStatus
from src.exceptions.auth import ExceptionUserAccountNotExists, ExceptionUserHasBlocked, ExceptionUserNotExists, TokenNotAccept
from src.helpers.jwt import gen_user_token, gen_refresh_token, check_refresh_token, remove_token
from src.models.user import UserModel
from bcrypt import checkpw
import bcrypt

class UserService(object):
    @staticmethod
    def gen_token_by_user(user_info: dict):
        """
            :param user_info
            :return token, refresh_token
        """
        token = gen_user_token(user_info=user_info)
        refresh_token = gen_refresh_token(token=token, obj_type='user_account')
        return token, refresh_token

    @classmethod
    def login(cls, phone: str, password: str):

        user = UserModel.get_with_key_sync(value=phone, key_sync='phone')
        if not user:
            raise ExceptionUserNotExists
        if user.get('status') == UserAccountStatus.BLOCKED:
            raise ExceptionUserHasBlocked
        
        # compare password
        if not checkpw(password.encode('utf8'), user.get('password').encode('utf8')):
            raise ExceptionUserAccountNotExists
        
        token, refresh_token = cls.gen_token_by_user(user_info=user)
        return {
            'token': token,
            'refresh_token': refresh_token
        }
    
    @classmethod
    def logout(cls, token: str):
        
        return True
    
    @staticmethod
    def regen_token(payload: dict, obj_type: str) -> tuple:
        token = None
        if obj_type == 'user_account':
            token = gen_user_token(user_info=payload)
        refresh_token = gen_refresh_token(token=token, obj_type=obj_type)
        return token, refresh_token
    
    @classmethod
    def refresh(cls, refresh_token: str, request_token: str, obj_type: str):
        _payload = get_token_info(refresh_token)
        if not isinstance(_payload, dict) or request_token != _payload.get('payload', {}).get('token'):
            raise TokenNotAccept
        
        if not check_refresh_token(token_refresh=refresh_token, obj_type=obj_type, is_delete=True):
            raise TokenNotAccept
        _old_payload = get_token_info(request_token)
        _payload = _old_payload.get('payload')

        remove_token(payload=_payload, obj_type=obj_type)
        token, refresh_token = cls.regen_token(payload=_payload, obj_type=obj_type)
        return {
            'token': token,
            'refresh_token': refresh_token
        }
    
    @classmethod
    def register(cls, name: str, phone: str, password: str, store_id: str, email: str, address: str, permission: str):

        _find_user = UserModel.check_is_exist(filter={
            'phone': phone
        }, with_cache=False)
        if _find_user == True:
            return 'ALREADY_EXISTS'
        else:
            _payload = {
                "name": name,
                "phone": phone,
                "password": bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10)).decode('utf-8'),
                "store_id": store_id,
                "email": email,
                "address": address,
                "permission": permission
            }
            result = UserModel.insert_data(payload=_payload)
            if result:
                return True
            return False
