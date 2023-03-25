# File model.py 
# Created at 25/03/2023
# Author Khanh

import traceback
from datetime import datetime

from bson import ObjectId
from pymodm import fields, MongoModel, connection

SIZE = 10000
class BaseModel(MongoModel):

    created_by = fields.CharField(default='', blank=True)
    updated_by = fields.CharField(default='', blank=True)
    created_time = fields.DateTimeField(default=None)
    updated_time = fields.DateTimeField(default=None)
    deleted = fields.BooleanField(default=False, blank=True)
    deleted_time = fields.DateTimeField(default=None, blank=True)

    @classmethod
    def current(cls):
        return connection._get_db(cls._mongometa.connection_alias)[cls._mongometa.collection_name]

    @classmethod
    def get_with_key_sync(cls,
                          value,
                          key_sync='_id',
                          db_name: str = 'teship',
                        #   with_cache=False,
                          one=True
                          ):
        try:
            _filter = {}
            if isinstance(key_sync, list):
                if not isinstance(value, dict):
                    raise Exception('Value must be dict with list keys_sync')
                key_sync.sort()
                _val_key = ':'.join([f'{x}:{(value.get(x))}' for x in key_sync])
                _filter = value
            else:
                _filter = {
                    key_sync: value
                }
                _val_key = value
            _key = f"teship:{db_name}/{cls.Meta.collection_name}:{_val_key}"

            def get_db():
                if one:
                    _row = cls.current().find_one(filter=_filter) or {}
                else:
                    _row = cls.current().find(filter=_filter) or []
                print('db row', _key, _row)
                return _row

            # cache in redis, will update later - khanh-note
            # if with_cache:
            #     @cache_key(key=_key)
            #     def get_cache():
            #         return get_db()

            #     return get_cache()
            return get_db()
        except cls.DoesNotExist:
            return {}
        except:
            # capture_exception()
            traceback.print_exc()
            return {}