import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from lib.models import BaseModelMixin
from lib.cipher import access_secret

from . import managers


class Account(BaseModelMixin):
    '''契約企業'''
    account_id = models.UUIDField(default=uuid.uuid4,
                                  unique=True,
                                  editable=False)
    name = models.CharField(max_length=100)
    access_key_id = models.CharField(max_length=32,
                                     default=access_secret,
                                     unique=True,
                                     editable=False)
    access_secret_key = models.CharField(max_length=32,
                                         default=access_secret,
                                         unique=True,
                                         editable=False)

    objects = managers.AccountManager()
    all_objects = managers.AccountManager(include_soft_deleted=True)

    class Meta:
        db_table = 'account'
        verbose_name = 'Account/契約企業'
        verbose_name_plural = 'Accounts/契約企業'
        indexes = [
            models.Index(fields=['account_id']),
            models.Index(fields=['name']),
            models.Index(fields=['access_key_id']),
        ]

    def __str__(self):
        return 'Account(name={})'.format(self.name)


class Member(BaseModelMixin, AbstractBaseUser, PermissionsMixin):
    '''企業メンバー'''
    # ユーザーの識別子
    member_id = models.UUIDField(default=uuid.uuid4,
                                unique=True,
                                editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.MemberManager()
    all_objects = managers.MemberManager(include_soft_deleted=True)

    def get_full_name(self):
        return self.full_name

    class Meta:
        db_table = 'member'
        verbose_name = 'Member/企業メンバー'
        verbose_name_plural = 'Members/企業メンバー'
        indexes = [
            models.Index(fields=['member_id']),
            models.Index(fields=['account']),
            models.Index(fields=['store']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return 'Member(email={}, full_name={}, account={})'.format(
            self.email,
            self.full_name,
            self.account.name,
        )
