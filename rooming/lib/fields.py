import datetime, time

from django.utils import timezone
from django.db import models

from livefield import LiveField


"""UnixTime
"""
def unix_timestamp():
    current_datetime = timezone.now()
    return int(current_datetime.timestamp())

class UnixTimeField(models.IntegerField):
    pass

class AutoCreatedField(UnixTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('db_index', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', unix_timestamp)
        super(AutoCreatedField, self).__init__(*args, **kwargs)

class AutoLastModifiedField(AutoCreatedField):
    def pre_save(self, model_instance, add):
        value = unix_timestamp()
        setattr(model_instance, self.attname, value)
        return value

class IndexedLiveField(LiveField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('db_index', True)
        super(IndexedLiveField, self).__init__(*args, **kwargs)
