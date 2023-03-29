# File urls.py 
# Created at 28/03/2023
# Author Khanh

from flask import Blueprint

from src.api.store.controlle import store_cr, get_list_store_by_ad

rest_store = Blueprint('rest_store', __name__, url_prefix='store')
rest_store.add_url_rule('store-cr', methods=['POST'], view_func=store_cr)
rest_store.add_url_rule('stores', methods=['GET'], view_func=get_list_store_by_ad)
