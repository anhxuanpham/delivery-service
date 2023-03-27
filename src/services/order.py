

from src.models.order import OrderModel

class OrderService(object):

    @staticmethod
    def save(payload: dict):
        # value = {
        #     **payload
        # }
        return OrderModel.insert_data(payload=payload)
    
    @staticmethod
    def get_list_order_by_filter(_id: str,
                                 offset: int,
                                 limit: int
                                ) -> list:
        filter = {}

        return True