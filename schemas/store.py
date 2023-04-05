# File store.py 
# Created at 28/03/2023
# Author Khanh

from marshmallow import Schema, EXCLUDE, INCLUDE, fields, pre_load

from vibe_library.schema import BaseResponse

class FormStoreCreateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True)
    address = fields.Str(required=True)
    phone = fields.Str(required=True)

    extract = fields.Dict(missing={}, allow_none=True)
    status = fields.Str(required=False)


class StoreResponseSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(allow_none=True)
    phone = fields.String(allow_none=True)
    address = fields.String(allow_none=True)

    wait_order = fields.Integer(allow_none=True)
    status = fields.String(allow_none=True)
    extract = fields.Dict(allow_none=True, missing={})
    created_time = fields.Float(required=True)


class GetListStoreResponseSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    stores = fields.List(fields.Nested(StoreResponseSchema()))
    total = fields.Integer()


class ReportByStoreSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE
    
    _id = fields.String(required=True)
    date = fields.String(required=True)
    
