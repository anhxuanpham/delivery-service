# File __init__.py 
# Created at 24/03/2023
# Author Khanh

from .user import rest_user
from .order import rest_order

rest_app = (
    rest_user,
    rest_order,
)