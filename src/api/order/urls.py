# File urls.py 
# Created at 27/03/2023
# Author Khanh

from flask import Blueprint
from src.api.order.controller import order_cr, get_list_order_by_store, get_detail_order

rest_order = Blueprint('rest_order', __name__, url_prefix='order')
rest_order.add_url_rule('order-cr', methods=['POST'], view_func=order_cr)
rest_order.add_url_rule('orders', methods=['GET'], view_func=get_list_order_by_store)
rest_order.add_url_rule('detail', methods=['GET'], view_func=get_detail_order)