import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField

from lib.models import BaseModelMixin
from . import managers


class Product(BaseModelMixin):
    '''商品'''
    product_id = models.UUIDField(default=uuid.uuid4,
                                  unique=True,
                                  editable=False)
    account = models.ForeignKey('accounts.Account',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    images = ArrayField(
        models.URLField(),
        size=20
    )
    description = models.TextField(null=True, default=None, blank=True)
    detail_url = models.TextField(null=True, default=None, blank=True)
    price = models.IntegerField(null=True, default=None, blank=True)
    release_date = models.URLField(null=True, default=None, blank=True)
    model = models.CharField(max_length=100,
                             null=True,
                             default=None,
                             blank=True)
    external_id = models.CharField(max_length=200,
                                   null=True,
                                   default=None,
                                   blank=True)
    search_vector = SearchVectorField(null=True)

    objects = managers.ProductManager()
    all_objects = managers.ProductManager(include_soft_deleted=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'Product/商品'
        verbose_name_plural = 'Products/商品'
        unique_together = (
            # ('title', 'live'),
            ('account', 'external_id', 'live'),
        )
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['account']),
            models.Index(fields=['title']),
            models.Index(fields=['price']),
            models.Index(fields=['release_date']),
            models.Index(fields=['external_id']),
            # 複合キー
            models.Index(fields=['product_id', 'account']),
        ]

    def __str__(self):
        return 'Product(title={}, account={}, price={})'.format(
            self.title, self.account and self.account.name, self.price)


class StoreProduct(BaseModelMixin):
    '''店舗商品関連'''
    store_product_id = models.UUIDField(default=uuid.uuid4,
                                        unique=True,
                                        editable=False)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    store = models.ForeignKey('accounts.Store', on_delete=models.CASCADE)
    num_stock = models.IntegerField()

    objects = managers.StoreProductManager()
    all_objects = managers.StoreProductManager(include_soft_deleted=True)

    class Meta:
        db_table = 'store_product'
        verbose_name = 'StoreProduct/店舗商品関連'
        verbose_name_plural = 'StoreProducts/店舗商品関連'
        indexes = [
            models.Index(fields=['store_product_id']),
            models.Index(fields=['product']),
            models.Index(fields=['store']),
        ]

    def __str__(self):
        return 'StoreProduct(product={}, store={}, num_stock={})'.format(
            self.product.title, self.store and self.store.name, self.num_stock)


class ProductFeature(BaseModelMixin):
    '''商品詳細情報'''
    feature_id = models.UUIDField(default=uuid.uuid4,
                                          unique=True,
                                          editable=False)
    label = models.CharField(max_length=100)

    objects = managers.ProductFeatureManager()
    all_objects = managers.ProductFeatureManager(include_soft_deleted=True)

    class Meta:
        db_table = 'product_feature'
        verbose_name = 'ProductFeatue/商品詳細情報'
        verbose_name_plural = 'ProductFeatues/商品詳細情報'
        indexes = [
            models.Index(fields=['feature_id']),
            models.Index(fields=['label']),
        ]


class ProductFeatureValue(BaseModelMixin):
    '''商品詳細情報値'''
    feature_value_id = models.UUIDField(default=uuid.uuid4,
                                          unique=True,
                                          editable=False)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    feature = models.ForeignKey('products.ProductFeature', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    objects = managers.ProductFeatureValueManager()
    all_objects = managers.ProductFeatureValueManager(include_soft_deleted=True)

    class Meta:
        db_table = 'product_feature_value'
        verbose_name = 'ProductFeatureValue/商品詳細情報値'
        verbose_name_plural = 'ProductFeatureValues/商品詳細情報値'
        indexes = [
            models.Index(fields=['feature_value_id']),
            models.Index(fields=['value']),
            # 複合キー
            models.Index(fields=['product', 'feature']),
        ]
