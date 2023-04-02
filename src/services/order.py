# File order.py 
# Created at 27/03/2023
# Author Khanh

from src.models.order import OrderModel
from bson import ObjectId
class OrderService(object):

    @staticmethod
    def save(payload: dict):
        # value = {
        #     **payload
        # }
        return OrderModel.insert_data(payload=payload)
    
    @staticmethod
    def get_list_orders(store_id: str,
                        offset: int,
                        limit: int
                        ) -> list:
        
        filter = {}
        if store_id:
            filter['store_id'] = store_id

        orders = OrderModel.get_by_filter(
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

        if len(orders) < limit:
            return orders, offset + len(orders)
        else:
            return orders, offset + limit + limit // 2
        
    
    @staticmethod
    def order_detail(_id: str):        
        order = OrderModel.get_by_id(_id, with_cache=False)
        return order

