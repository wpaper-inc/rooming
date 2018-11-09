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
    line_user_id = models.UUIDField(unique=True, editable=False)
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
