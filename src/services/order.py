# File order.py 
# Created at 27/03/2023
# Author Khanh

from src.models.order import OrderModel

class OrderService(object):

    @staticmethod
    def save(payload: dict):
        # value = {
        #     **payload
        # }
        return OrderModel.insert_data(payload=payload)
    
    @staticmethod
    def get_list_orders(_id: str,
                        offset: int,
                        limit: int
                        ) -> list:
        
        filter = {}
        if _id:
            filter['store_id'] = _id

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
        