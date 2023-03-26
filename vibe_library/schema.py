import traceback
from datetime import datetime
from datetime import timezone
import sentry_sdk
import six
from marshmallow import pre_load, fields
from collections import OrderedDict

@six.python_2_unicode_compatible
class Message(object):
    """
    Data that is published as a server-sent event.
    """

    def __init__(self, data, type=None, id=None, retry=None):
        """
        Create a server-sent event.

        :param data: The event data. If it is not a string, it will be
            serialized to JSON using the Flask application's
            :class:`~flask.json.JSONEncoder`.
        :param type: An optional event type.
        :param id: An optional event ID.
        :param retry: An optional integer, to specify the reconnect time for
            disconnected clients of this stream.
        """
        self.data = data
        self.type = type
        self.id = id
        self.retry = retry

    def to_dict(self):
        """
        Serialize this object to a minimal dictionary, for storing in Redis.
        """
        # data is required, all others are optional
        d = {"data": self.data}
        if self.type:
            d["type"] = self.type
        if self.id:
            d["id"] = self.id
        if self.retry:
            d["retry"] = self.retry
        return d

    def __str__(self):
        """
        Serialize this object to a string, according to the `server-sent events
        specification <https://www.w3.org/TR/eventsource/>`_.
        """
        if isinstance(self.data, six.string_types):
            data = self.data
        else:
            data = dumps(self.data)
        lines = ["data:{value}".format(value=line) for line in data.splitlines()]
        if self.type:
            lines.insert(0, "event:{value}".format(value=self.type))
        if self.id:
            lines.append("id:{value}".format(value=self.id))
        if self.retry:
            lines.append("retry:{value}".format(value=self.retry))
        return "\n".join(lines) + "\n\n"

    def __repr__(self):
        kwargs = OrderedDict()
        if self.type:
            kwargs["type"] = self.type
        if self.id:
            kwargs["id"] = self.id
        if self.retry:
            kwargs["retry"] = self.retry
        kwargs_repr = "".join(
            ", {key}={value!r}".format(key=key, value=value)
            for key, value in kwargs.items()
        )
        return "{classname}({data!r}{kwargs})".format(
            classname=self.__class__.__name__,
            data=self.data,
            kwargs=kwargs_repr,
        )

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__) and
                self.data == other.data and
                self.type == other.type and
                self.id == other.id and
                self.retry == other.retry
        )
    

class BaseResponse():
    @pre_load
    def load_id(self, in_data, **kwargs):
        if in_data.get('_id'):
            in_data['_id'] = str(in_data['_id'])
        return in_data

    @pre_load
    def load_datetime(self, in_data, **kwargs):
        for key, value in in_data.items():
            if isinstance(value, datetime):
                in_data[key] = value.replace(tzinfo=timezone.utc).timestamp()
        return in_data

    @classmethod
    def load_response(cls, payload: dict = {}):
        try:
            try:
                result = cls().load(payload)
                return result
            except:
                sentry_sdk.capture_exception()
                traceback.print_exc()
                return {}
        except:
            sentry_sdk.capture_exception()
            traceback.print_exc()
