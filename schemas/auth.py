# File auth.py 
# Created at 25/03/2023
# Author Khanh

from marshmallow import Schema, EXCLUDE, fields, pre_load

from vibe_library.schema import BaseResponse

class FormUserLoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    phone = fields.Str(required=True)
    password = fields.Str(required=True)
    
class UserAuthSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)
