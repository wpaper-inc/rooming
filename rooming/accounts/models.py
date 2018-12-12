import uuid
import functools

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from lib.models import BaseModelMixin
from lib.cipher import generate_secret

from . import managers


class Account(BaseModelMixin):
    '''契約企業'''
    account_id = models.UUIDField(default=uuid.uuid4,
                                  unique=True,
                                  editable=False)
    name = models.CharField(max_length=100)
    public_key = models.CharField(max_length=35,
                                     default=functools.partial(generate_secret, 'pb'),
                                     unique=True,
                                     editable=False)
    secret_key = models.CharField(max_length=35,
                                         default=functools.partial(generate_secret, 'sk'),
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
            models.Index(fields=['public_key']),
            models.Index(fields=['secret_key']),
        ]

    def __str__(self):
        return 'Account(name={})'.format(self.name)


class TrackingURL(BaseModelMixin):
    '''外部URLへアクセスしたことを検知する短縮URL'''
    tracking_url_id = models.UUIDField(default=uuid.uuid4,
                                unique=True,
                                editable=False)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    url = models.URLField(max_length=1024, unique=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    click_count = models.IntegerField(default=0)

    objects = managers.AccountManager()
    all_objects = managers.AccountManager(include_soft_deleted=True)

    class Meta:
        db_table = 'tracking_url'
        verbose_name = 'TrackingURL/短縮URL'
        verbose_name_plural = 'TrackingURLs/短縮URL'
        unique_together = ('account', 'user', 'url', 'live')
        indexes = [
            models.Index(fields=['tracking_url_id']),
            models.Index(fields=['account']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return 'TrackingURL(id={})'.format(self.tracking_url_id)


class Store(BaseModelMixin):
    '''店舗'''
    store_id = models.UUIDField(default=uuid.uuid4,
                                unique=True,
                                editable=False)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)

    objects = managers.StoreManager()
    all_objects = managers.StoreManager(include_soft_deleted=True)

    class Meta:
        db_table = 'store'
        verbose_name = 'Store/店舗'
        verbose_name_plural = 'Stores/店舗'
        indexes = [
            models.Index(fields=['store_id']),
            models.Index(fields=['account']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return 'Store(name={})'.format(self.name)


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
    store = models.ForeignKey('accounts.Store', null=True, default=None, on_delete=models.CASCADE)

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
