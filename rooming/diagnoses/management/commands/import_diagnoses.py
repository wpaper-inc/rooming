import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from accounts.models import Account
from diagnoses.services import DiagnosisService


class Command(BaseCommand):
    help = '診断Excelフォーマットの一括取り込み'

    def add_arguments(self, parser):
        parser.add_argument('file', help='Excelファイル')

    def handle(self, *args, **options):
        BASE_NAME = os.path.abspath(os.path.dirname(__file__))
        filename = options.get('file')
        filepath = os.path.join(BASE_NAME, filename)
        account, created = Account.objects.get_or_create(name='mizuno')
        service = DiagnosisService(account)
        service.import_excel(filepath)
