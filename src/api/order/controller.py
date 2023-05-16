# File controller.py 
# Created at 27/03/2023
# Author Khanh

import bcrypt
from flask import g, request
from schemas.order import FormOrderCreateSchema, FormGetOrdersSchema, GetAllOrderResponseSchema, GetListOrderResponseSchema, OrderDetalResponseSchema, UpdateStatusOrderSchema
from src.exceptions.auth import InvalidAdminPermission
from src.services.order import OrderService
from src.services.user import UserService
import vibe_library.decorators as deco

from vibe_library.handlerespon import make_response

@deco.handle_response()
@deco.load_data(FormOrderCreateSchema)
@deco.auth_user()
def order_cr(user):
    """
        - Control the create action of order  
    """
    order_data = g.data
    result = OrderService.save(payload=order_data)
    if result:
        return True
    else:
        return False


@deco.handle_response()
@deco.auth_user()
def get_list_order_by_store(user):

    store_id = request.args.get('store_id', '', type=str)
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    orders, total = OrderService.get_list_orders(store_id=store_id, offset=offset, limit=limit)
    if not isinstance(orders, list):
        orders = []
    
    return GetListOrderResponseSchema.load_response({
        'orders': orders,
        'total': total
    })

@deco.handle_response()
@deco.auth_user()
def get_detail_order(user):

    id = request.args.get('id', '', type=str)
    order = OrderService.order_detail(_id=id)
    return OrderDetalResponseSchema.load_response(order)


@deco.handle_response()
@deco.load_data(UpdateStatusOrderSchema)
@deco.auth_user()
def update_status(user):
    _data = g.data 
    _id = _data.get('_id')
    status = _data.get('status')
    message = _data.get('message', '')

    result = OrderService.update_order(_id=_id, status=status, message=message)
    return result


@deco.handle_response()
@deco.auth_user()
def get_list_order_by_admin(user):
    if user.get('permission') != 'admin':
        raise InvalidAdminPermission

    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    status = request.args.get('status', '', type=str)

    orders, order_total, total = OrderService.get_all_list_orders(status=status, offset=offset, limit=limit)
    return GetAllOrderResponseSchema.load_response({
        'orders': orders,
        'order_total': order_total,
        'total': total
    })