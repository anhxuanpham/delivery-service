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
            def get_db():
                _query = [{
                    '$match' : filter
                }]
                if 'sort' in __option_keys:
                    _query.append({
                        '$sort': options.get('sort')
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
        
    @classmethod
    def update_one(cls, filter, update_data):
        try:
            _keys = update_data.keys()
            _delete_keys = ['created_by', 'created_time', '_id']
            for _key in _delete_keys:
                if _key in _keys:
                    del update_data[_key]
            update_data['updated_time'] = get_current_time()
            return cls.current().find_one_and_update(filter=filter, update={
                '$set': update_data
            })
        except cls.DoesNotExist:
            return []
        # except Exception as e:
        #     capture_exception(e)
        #     traceback.print_exc()
        #     return []


    @classmethod
    def get_by_id(cls, _id, with_cache=True):
        try:
            def get_db():
                try:
                    value = cls.objects.values().get({'_id': fields.ObjectId(_id)})
                    if value:
                        if not value.get('deleted'):
                            return value
                        # _json_value = value.to_dict()
                        # if not _json_value.get('deleted'):
                        #     return _json_value
                        # if 
                        return value
                    return {}
                except cls.DoesNotExist:
                    return {}
                except:
                    traceback.print_exc()
                return {}

            # if with_cache:
            #     @cache_id(key_prefix=cls.Meta.collection_name)
            #     def get_cache_by_id(with_id):
            #         return get_db()

            #     return get_cache_by_id(_id)
            return get_db()
        except:
            traceback.print_exc()
            return {}

    @classmethod
    def get_one(cls, filter, with_cache=False):
        try:
            _keys = list(filter.keys())

            def get_db():
                value = cls.objects.get(filter)
                if value:
                    _json_value = value.to_dict()
                    if not _json_value.get('deleted'):
                        return _json_value
                return {}

            # if with_cache:
            #     @cache_filter(key_prefix=cls.Meta.collection_name, key_fields=_keys, options=[])
            #     def get_cache_by_filter(*args, **kwargs):
            #         return get_db()

            #     return get_cache_by_filter(**filter, options=[])
            return get_db()

        except cls.DoesNotExist:
            return {}
        except:
            # capture_exception()
            traceback.print_exc()
            return {}
    