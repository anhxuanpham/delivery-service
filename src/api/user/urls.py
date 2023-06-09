# File urls.py 
# Created at 24/03/2023
# Author Khanh

from flask import Blueprint

from src.api.user.controller import login_cl, register_cl, refresh_token_cl, logout_cl

rest_user = Blueprint('rest_user', __name__, url_prefix='user')
rest_user.add_url_rule('login', methods=['POST'], view_func=login_cl)
rest_user.add_url_rule('register', methods=['POST'], view_func=register_cl)
rest_user.add_url_rule('refresh-token', methods=['POST'], view_func=refresh_token_cl)
rest_user.add_url_rule('sign-out', methods=['GET'], view_func=logout_cl)
