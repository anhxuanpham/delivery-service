# File ultilities.py
# Created at 26/03/2023
# Author Khanh

import json
import traceback
from datetime import datetime, timezone

from bson import ObjectId

def get_current_time():
    return datetime.utcnow().replace(tzinfo=timezone.utc)

def json_decode_hook(obj):
    if '__datetime__' in obj:
        return datetime.strptime(obj['as_str'], "%Y%m%dT%H:%M:%S.%f")
    if b'__datetime__' in obj:
        return datetime.strptime(obj[b'as_str'], "%Y%m%dT%H:%M:%S.%f")
    return obj

def is_oid(oid):
    return ObjectId.is_valid(oid)