# File order.py 
# Created at 27/03/2023
# Author Khanh

from marshmallow import Schema, EXCLUDE, INCLUDE, fields, pre_load

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


class ProductOrderResponse(Schema, BaseResponse):
    class Meta:
        unknown: EXCLUDE

    product_name = fields.String(allow_none=True)
    product_price = fields.Float(allow_none=True)
    quantity = fields.Integer(allow_none=True)

class OrderDetalResponseSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE
    _id = fields.String(required=True)
    cust_name = fields.String(allow_none=True)
    cust_phone = fields.String(allow_none=True)
    address = fields.String(allow_none=True)

    store_id = fields.String(allow_none=True)
    user_id = fields.String(allow_none=True)
    product_list = fields.List(fields.Nested(ProductOrderResponse()))
    fee_ship = fields.Float(required=True)
    order_code = fields.String(allow_none=True)

    total_amount = fields.Float(required=True)
    status = fields.String(allow_none=True)
    extract = fields.Dict(allow_none=True, missing={})
    created_time = fields.Float(required=True)

class OrderResponseSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE
    
    _id = fields.String(required=True)
    cust_name = fields.String(allow_none=True)
    cust_phone = fields.String(allow_none=True)
    address = fields.String(allow_none=True)

    store_id = fields.String(allow_none=True)
    user_id = fields.String(allow_none=True)
    # product_list = fields.List(fields.Nested(ProductOrderResponse()))
    fee_ship = fields.Float(required=True)
    # order_code = fields.String(allow_none=True)

    total_amount = fields.Float(required=True)
    status = fields.String(allow_none=True)
    # extract = fields.Dict(allow_none=True, missing={})
    created_time = fields.Float(required=True)


class GetListOrderResponseSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE
    
    orders = fields.List(fields.Nested(OrderResponseSchema()))
    total = fields.Integer()

class GetAllOrderResponseSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE
    
    orders = fields.List(fields.Nested(OrderResponseSchema()))
    order_total = fields.Integer()
    total = fields.Integer()

class UpdateStatusOrderSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE
    
    _id = fields.String(required=True)
    status = fields.String(required=True)
    message = fields.String(required=False)
