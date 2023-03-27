# File controller.py 
# Created at 27/03/2023
# Author Khanh

import bcrypt
from flask import g, request
from schemas.order import FormOrderCreateSchema, FormGetOrdersSchema
from src.services.order import OrderService
from src.services.user import UserService
import vibe_library.decorators as deco

from vibe_library.handlerespon import make_response

@deco.handle_response()
@deco.load_data(FormOrderCreateSchema)
def order_cr():
    """
        - Control the create action of order  
    """
    order_data = g.data
    print('---order----', order_data)
    result = OrderService.save(payload=order_data)
    if result:
        return True
    else:
        return False


@deco.handle_response()
def get_list_order_by_store():

    _id = request.args.get('_id', '', type=str)
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    # orders, total = 
    return 'list order by store'