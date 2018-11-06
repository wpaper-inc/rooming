import datetime

from django.db import models

from .fields import (
    AutoCreatedField,
    AutoLastModifiedField,
    IndexedLiveField,
)


class UnixTimestampedModelMixin(models.Model):
    created_at = AutoCreatedField()
    updated_at = AutoLastModifiedField()

    class Meta:
        abstract = True

    @property
    def created_datetime(self):
        return datetime.datetime.fromtimestamp(self.created_at)

    @property
    def updated_datetime(self):
        return datetime.datetime.fromtimestamp(self.updated_at)

class LiveModelMixin(models.Model):
    live = IndexedLiveField()

    def delete(self, using=None):
        self.live = False
        self.save(using=using)

    class Meta:
        abstract = True


class BaseModelMixin(UnixTimestampedModelMixin, LiveModelMixin):
    class Meta:
        abstract = True
