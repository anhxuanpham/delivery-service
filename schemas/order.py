# File order.py 
# Created at 27/03/2023
# Author Khanh

from marshmallow import Schema, EXCLUDE, fields, pre_load

from vibe_library.schema import BaseResponse

class FormOrderCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    cust_name = fields.Str(required=True)
    cust_phone = fields.Str(required=True)
    store_id = fields.Str(required=True)
    user_id = fields.Str(required=True)

    address = fields.Str(required=True)
    product_list = fields.List(fields.Dict, missing=[])
    total_amount = fields.Float(required=True)
    fee_ship = fields.Float(required=True)
    
    extract = fields.Dict(missing={}, allow_none=True)
    status = fields.Str(required=True)

class FormGetOrdersSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    _id = fields.Str(required=True)