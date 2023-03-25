# File extensions.py 
# Created at 25/03/2023
# Author Khanh

import json
import redis
import os
from dotenv import load_dotenv

load_dotenv()

pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=10)
redis_single = redis.Redis(connection_pool=pool)
