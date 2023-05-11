# File config.py 
# Created at 24/03/2023
# Author Khanh

import os
import json
from dotenv import load_dotenv

load_dotenv()
class BaseConfig(object):
    
    PROJECT = 'delivery-service'
    DEBUG = False
    TESTING = False

class DefaultConfig(BaseConfig):
    DEBUG = True
    PREFIX = f'/v1/{BaseConfig.PROJECT}'
    ACCEPT_LANGUAGES = ['vi']
    BABEL_DEFAULT_LOCALE = 'en'

    MONGODB_URI = os.getenv('MONGODB_URI')
    

    # seconds expired
    TOKEN_EXP_TIME = int(os.getenv('TOKEN_EXP_TIME', default=86400))
    # seconds expired
    REFRESH_TOKEN_EXP_TIME = os.getenv('REFRESH_TOKEN_EXP_TIME', default=180)