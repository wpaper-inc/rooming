import io
import os
import json
import csv

from django.test import TestCase
from django.core import management

from accounts.models import Member
from products.models import Product
from products.services import UploadProductsCSVService


class ProductServiceTest(TestCase):
    def setUp(self):
        management.call_command('initialize_app')

        self.account = Member.objects.get(email=os.getenv('SUPER_MEMBER_EMAIL')).account
        self.filename = os.path.join(os.path.dirname(__file__), 'seed_product.csv')

    def import_product_test(self):
        with open(self.filename, 'rb') as fp:
            service = UploadProductsCSVService(fp, self.account)
            service.import_csv()

        with open(self.filename, 'rb') as fp:
            reader = csv.reader(io.TextIOWrapper(fp))
            header = next(reader)

            for row in reader:
                # 商品名,画像,詳細,税込み価格,発売日,型番,外部ID
                title = row[0]
                images = row[1].split('$$')
                description = row[2]
                price = row[3].replace(',', '')
                release_date = row[4]
                model = row[5]
                external_id = row[6]
                try:
                    product = Product.objects.get(external_id=external_id)
                except Product.DoesNotExists as exc:
                    self.fail(exc)
                self.assertTrue(product.title, title)
                self.assertTrue(product.description, description)
                self.assertTrue(product.images, images)
                self.assertTrue(product.price, price)
                self.assertTrue(product.release_date, release_date)
                self.assertTrue(product.model, model)
