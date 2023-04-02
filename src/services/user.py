# File user.py 
# Created at 24/03/2023
# Author Khanh

from src.enums.user import UserAccountStatus
from src.exceptions.auth import ExceptionUserAccountNotExists, ExceptionUserHasBlocked, ExceptionUserNotExists
from src.helpers.jwt import gen_user_token, gen_refresh_token
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
