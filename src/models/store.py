# File store.py
# Created at 28/03/2023
# Author Khanh

from vibe_library.model import BaseModel
from pymodm import fields

class StoreModel(BaseModel):
    class Meta:
        collection_name = 'teship_stores'
        final = True
        ignore_unknown_fields = True
    
    _id = fields.ObjectIdField(primary_key=True)
    name = fields.CharField(blank=True, default='')
    phone = fields.CharField(blank=True, default='')
    address = fields.CharField(blank=True, default='')
    
    wait_order = fields.IntegerField(blank=True, default=0)
    extract = fields.DictField(blank=True, default={})
    status = fields.CharField(default='active', blank=True)
    