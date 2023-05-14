# File user.py 
# Created at 28/03/2023
# Author Khanh

from src.exceptions.store import ExceptionStoreExists
from src.models.store import StoreModel
from src.models.order import OrderModel


class StoreService(object):

    @classmethod
    def save(cls, payload: dict):
        # value = {
        #     **payload
        # }
        _phone = payload.get('phone')
        find_store = StoreModel.check_is_exist(filter={
            'phone': _phone
        }, with_cache=False)

        if find_store == True:
            raise ExceptionStoreExists
        else:
            return StoreModel.insert_data(payload=payload)
    
    @classmethod
    def get_list_stores( self ,offset: int, limit: int ) -> list:
        
        stores_update = self.get_stores(offset=offset, limit=limit)
        for store in stores_update:

            _store_id = store.get('_id')
            filter = {}
            if _store_id:
                filter['store_id'] = str(_store_id)
                filter['status'] = 'wait'

            wait_order_count = len(OrderModel.get_by_filter(filter=filter, options={}, with_cache=False))

            if store.get('wait_order') != wait_order_count:
                StoreModel.update_one(
                    filter={
                        '_id': store.get('_id')
                    },
                    update_data= {
                        **store,
                        'wait_order': wait_order_count
                    }
                )

        stores = self.get_stores(offset=offset, limit=limit)

        store_total = StoreModel.total_count()
        if len(stores) < limit:
            return stores, store_total, offset + len(stores)
        else:
            return stores, store_total, offset + limit + limit // 2


    @staticmethod
    def get_stores( offset: int, limit: int ) -> list:
        filter = {}
        stores = StoreModel.get_by_filter(
            filter=filter,
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            },
            with_cache=False
        )
        return stores
    
    @staticmethod
    def get_order_by_filter(start_day, end_day, store_id):

        filter = {}
        filter['created_time'] = {
            "$gte": start_day,
            "$lt": end_day
        }
        if store_id:
            filter['store_id'] = {
                '$in': [store_id],
            }

        orders = OrderModel.get_by_filter(filter=filter,options={},with_cache=False)

        total_amount = 0
        total_order = len(orders)
        order_success = 0
        order_fail = 0
        ship = 0

        if total_order > 0:
            for order in orders:
                total_amount = total_amount + order.get('total_amount')
                ship = ship + order.get('fee_ship')
                if order.get('status') == 'success':
                    order_success+=1
                if order.get('status') == 'fail':
                    order_fail+=1
                
        return {
            "total_amount": total_amount,
            "total_order": total_order,
            "order_success": order_success,
            "order_fail": order_fail,
            "ship" : ship
        }