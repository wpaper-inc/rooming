import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField

from lib.models import BaseModelMixin
from . import managers


class User(BaseModelMixin):
    '''ユーザー'''
    user_id = models.UUIDField(default=uuid.uuid4,
                               unique=True,
                               editable=False)
    line_user_id = models.CharField(max_length=200, null=True, default=None)
    full_name = models.CharField(max_length=150, null=True, default=None)

    objects = managers.UserManager()
    all_objects = managers.UserManager(include_soft_deleted=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'User/ユーザー'
        verbose_name_plural = 'Users/ユーザー'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['line_user_id']),
        ]


class Activity(BaseModelMixin):
    '''ユーザーのアクセスログ'''
    activity_id = models.UUIDField(default=uuid.uuid4,
                                   unique=True,
                                   editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    path = models.CharField(max_length=1024)
    params = JSONField(max_length=1024)
    action = models.CharField(max_length=100, null=True, default=None, blank=True)
    action_id = models.CharField(max_length=256, null=True, default=None, blank=True)
    account = models.ForeignKey('accounts.Account',
                                null=True,
                                default=None,
                                on_delete=models.CASCADE)

    objects = managers.ActivityManager()
    all_objects = managers.ActivityManager(include_soft_deleted=True)

    class Meta:
        db_table = 'activity'
        verbose_name = 'Activity/ユーザーアクセスログ'
        verbose_name_plural = 'Activities/ユーザーアクセスログ'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['path']),
            models.Index(fields=['user', 'path']),
        ]


class AccountUser(BaseModelMixin):
    '''企業ユーザー'''
    account_user_id = models.UUIDField(default=uuid.uuid4,
                                       unique=True,
                                       editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)

    objects = managers.AccountUserManager()
    all_objects = managers.AccountUserManager(include_soft_deleted=True)

    class Meta:
        db_table = 'account_user'
        verbose_name = 'AccountUser/企業ユーザー'
        verbose_name_plural = 'AccountUsers/企業ユーザー'
        unique_together = ('user', 'account', 'live')
        indexes = [
            models.Index(fields=['account_user_id']),
            models.Index(fields=['user']),
            models.Index(fields=['account']),
        ]
