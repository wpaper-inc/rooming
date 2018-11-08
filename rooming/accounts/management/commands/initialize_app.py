import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from accounts.models import (
    Account,
    Store,
    Member,
)


class Command(BaseCommand):
    help = 'スーパー管理ユーザーの作成、テスト用ダミーデータの作成'

    def handle(self, *args, **options):
        # スーパーアカウント(Whitepaper)
        super_account, created = Account.objects.get_or_create(name='Mefilas')
        # スーパーメンバー(WebMaster)
        sm_email = os.getenv('SUPER_MEMBER_EMAIL')
        sm_password = os.getenv('SUPER_MEMBER_PASSWORD')
        try:
            super_member = Member.objects.get(
                email=sm_email,
                account=super_account)
        except Member.DoesNotExist:
            super_member = Member.objects.create_superuser(
                email=sm_email,
                password=sm_password,
                account=super_account,
                full_name='webmaster')
        # 店舗を追加
        store, created = Store.objects.get_or_create(
            account=super_account,
            name='大阪本社')
        if not super_member.store:
            super_member.store = store
            super_member.save()
