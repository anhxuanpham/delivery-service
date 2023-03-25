# File auth.py 
# Created at 25/03/2023
# Author Khanh

from marshmallow import Schema, EXCLUDE, fields, pre_load

class FormUserLoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    
    phone = fields.Str(required=True)
    password = fields.Str(required=True)
    