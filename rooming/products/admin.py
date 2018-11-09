from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    pass

class StoreProductAdmin(admin.ModelAdmin):
    pass

class ProductFeatureAdmin(admin.ModelAdmin):
    pass

class ProductFeatureValueAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.StoreProduct, StoreProductAdmin)
admin.site.register(models.ProductFeature, ProductFeatureAdmin)
admin.site.register(models.ProductFeatureValue, ProductFeatureValueAdmin)
