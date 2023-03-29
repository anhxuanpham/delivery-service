# File user.py 
# Created at 28/03/2023
# Author Khanh

from src.models.store import StoreModel
from src.models.order import OrderModel


class StoreService(object):

    @staticmethod
    def save(payload: dict):
        # value = {
        #     **payload
        # }
        return StoreModel.insert_data(payload=payload)
    
    @staticmethod
    def get_list_stores(offset: int,
                        limit: int
                        ) -> list:
        
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
        for store in stores:

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

        if len(stores) < limit:
            return stores, offset + len(stores)
        else:
            return stores, offset + limit + limit // 2


