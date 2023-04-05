# File controller.py 
# Created at 28/03/2023
# Author Khanh

import bcrypt
from flask import g, request
from schemas.store import FormStoreCreateSchema, GetListStoreResponseSchema, ReportByStoreSchema
from src.services.store import StoreService
import vibe_library.decorators as deco
import datetime

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


@deco.handle_response()
@deco.load_data(ReportByStoreSchema)
def report_by_store():
    _data = g.data
    _day = _data.get('date')
    _test = f'{_day}T00:00:00'

    day = datetime.datetime.strptime(_test, '%Y-%m-%dT%H:%M:%S')
    start_day = day - datetime.timedelta(hours=7, minutes=0)

    end_day = day.replace(hour=23, minute=59, second=59, microsecond=999999) - datetime.timedelta(hours=7, minutes=0)
    store_id = _data.get('_id')
    result = StoreService.get_order_by_filter(start_day=start_day, end_day=end_day, store_id= store_id)

    print('------result-----', result)
    return result

