# File order.py
# Created at 26/03/2023
# Author Khanh

from vibe_library.model import BaseModel
from pymodm import fields

class OrderModel(BaseModel):
    class Meta:
        collection_name = 'teship_orders'
        final = True
        ignore_unknown_fields = True
    
    _id = fields.ObjectIdField(primary_key=True)
    cust_name = fields.CharField(default='', blank=True)
    cust_phone = fields.CharField(default='', blank=True)
    address = fields.CharField(default='', blank=True)

    store_id = fields.CharField(default='', blank=True)
    user_id = fields.CharField(default='', blank=True)
    product_list = fields.ListField(default=[], blank=True)
    total_amount = fields.FloatField(blank=True, default='')
    fee_ship = fields.FloatField(blank=True, default='')

    order_code = fields.CharField(default='', blank=True)
    extract = fields.DictField(blank=True, default={})
    status = fields.CharField(default='', blank=True)
