# File model.py 
# Created at 25/03/2023
# Author Khanh

import traceback
from datetime import datetime

from bson import ObjectId
from pymodm import fields, MongoModel, connection
from .utilities import is_oid, get_current_time

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
                          db_name: str = 'vibe',
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
            _key = f"vibe:{db_name}/{cls.Meta.collection_name}:{_val_key}"

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
    
    @classmethod
    def init_row(cls, payload):
        _init = {}
        for field in cls._mongometa.get_fields():
            if field.mongo_name == '_id':
                if not isinstance(payload.get('_id'), ObjectId):
                    if is_oid(payload.get(field.mongo_name)):
                        _init[field.mongo_name] = ObjectId(payload.get(field.mongo_name))
                    else:
                        _init[field.mongo_name] = ObjectId()
            else:
                if field.mongo_name in ['created_time', 'updated_time']:
                    if not isinstance(field.mongo_name, datetime):
                        if isinstance(field.mongo_name, (float, int)):
                            _init[field.mongo_name] = datetime.fromtimestamp()
                        else: 
                            _init[field.mongo_name] = get_current_time()
                else:
                    _init[field.mongo_name] = payload.get(field.mongo_name, field.default)
        return _init

    @classmethod
    def insert_data(cls, payload):
        return cls(**cls.init_row(payload)).save()
    
    @classmethod
    def get_by_filter(cls, filter={}, options={}, with_cache=False):
        try:
            _keys = list(filter.keys())
            __option_keys = list(options.keys())
            print('------_keys----', _keys)
            print('------_option_keys----', __option_keys)
            def get_db():
                _query = [{
                    '$match' : filter
                }]
                if 'sort' in __option_keys:
                    _query.append({
                        '$sort': __option_keys.get('sort')
                    })
                if 'offset' in __option_keys:
                    _query.append({
                        '$skip': options.get('offset')
                    })
                if 'limit' in __option_keys:
                    _query.append({
                        '$limit': options.get('limit')
                    })
                values = cls.objects.aggregate(*_query)
                values = list(values)
                return [x for x in values if not x.get('deleted')]
            
            return get_db()
        
        except cls.DoesNotExist:
            return {}
