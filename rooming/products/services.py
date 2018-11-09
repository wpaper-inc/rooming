import csv
import io

from django.db.utils import IntegrityError

from .models import Product


class UploadProductsCSVService(object):
    def __init__(self, file, account):
        self.csvfile = io.TextIOWrapper(file)
        self.account = account

    def import_csv(self):
        reader = csv.reader(self.csvfile)
        header = next(reader)
        for row in reader:
            product = Product(
                account=self.account,
                title=row[0],
                images=row[1].split('$$'),
                description=row[2],
                price=row[3].replace(',', ''),
                release_date=row[4],
                model=row[5],
                external_id=row[6],
            )
            try:
                product.save()
            except IntegrityError as err:
                print(err)
