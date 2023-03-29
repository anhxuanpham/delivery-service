# File controller.py 
# Created at 28/03/2023
# Author Khanh

import bcrypt
from flask import g, request
from schemas.store import FormStoreCreateSchema, GetListStoreResponseSchema
from src.services.store import StoreService
import vibe_library.decorators as deco

@deco.handle_response()
@deco.load_data(FormStoreCreateSchema)
def store_cr():

    _data = g.data
    result = StoreService.save(payload=_data)
    if result:
        return True
    else: return False

@deco.handle_response()
def get_list_store_by_ad():

    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    stores, total = StoreService.get_list_stores(offset=offset, limit=limit)

    if not isinstance(stores, list):
        stores = []
    
    return GetListStoreResponseSchema.load_response({
        'stores': stores,
        'total': total
    })
