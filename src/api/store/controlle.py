# File controller.py 
# Created at 28/03/2023
# Author Khanh

from dateutil import parser
import bcrypt
from flask import g, request
from schemas.store import FormStoreCreateSchema, GetListStoreResponseSchema, ReportByStoreSchema
from src.exceptions.auth import InvalidDateFormat
from src.services.store import StoreService
import vibe_library.decorators as deco
import datetime

@deco.handle_response()
@deco.load_data(FormStoreCreateSchema)
@deco.auth_user()
def store_cr(user):

    _data = g.data
    result = StoreService.save(payload=_data)
    if result:
        return True
    else: return False

@deco.handle_response()
@deco.auth_user()
def get_list_store_by_ad(user):

    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    stores, store_total, total = StoreService.get_list_stores(offset=offset, limit=limit)

    if not isinstance(stores, list):
        stores = []
    
    return GetListStoreResponseSchema.load_response({
        'stores': stores,
        'store_total': store_total,
        'total': total
    })


@deco.handle_response()
@deco.load_data(ReportByStoreSchema)
def report_by_store():
    _data = g.data
    _day = _data.get('date')

    isValidDate = True
    try:
        datetime.datetime.strptime(_day, '%Y-%m-%d')
    except ValueError:
        isValidDate = False
    
    if isValidDate:
        _date_timestamp = f'{_day}T00:00:00' 
        day = datetime.datetime.strptime(_date_timestamp, '%Y-%m-%dT%H:%M:%S')
    else:
        raise InvalidDateFormat
    
    start_day = day - datetime.timedelta(hours=7, minutes=0)

    end_day = day.replace(hour=23, minute=59, second=59, microsecond=999999) - datetime.timedelta(hours=7, minutes=0)
    store_id = _data.get('_id')
    result = StoreService.get_order_by_filter(start_day=start_day, end_day=end_day, store_id= store_id)

    print('-----result-----', result)
    return result

