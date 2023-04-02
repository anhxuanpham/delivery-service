# File model.py 
# Created at 24/03/2023
# Author Khanh

from vibe_library.model import BaseModel
from pymodm import fields

class UserModel(BaseModel):
    class Meta:
        collection_name = 'teship_users'
        final = True
        ignore_unknown_fields = True
    
    _id = fields.ObjectIdField(primary_key=True)
    name = fields.CharField(default='', blank=True)
    store_id = fields.CharField(default='', blank=True)
    phone = fields.CharField(default='', blank=True)
    email = fields.CharField(default='', blank=True)
    address = fields.CharField(default='', blank=True)
    password = fields.CharField(default='', blank=True)
    permission = fields.CharField(default='', blank=True)
    status = fields.CharField(default='active', blank=True)
