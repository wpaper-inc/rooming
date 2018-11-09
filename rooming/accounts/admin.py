from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'account_id',
        'name', 'public_key', 'secret_key',
    )

class StoreAdmin(admin.ModelAdmin):
    def account_name(self, obj):
        if obj.account:
            return obj.account.name
        return ''
    account_name.description = 'account'
    list_display = (
        'id', 'store_id',
        'name', 'account_name',
    )

class MemberAdmin(admin.ModelAdmin):
    def account_name(self, obj):
        if obj.account:
            return obj.account.name
        return ''
    account_name.description = 'account'
    def store_name(self, obj):
        if obj.store:
            return obj.store.name
        return ''
    store_name.description = 'store'
    list_display = (
        'id', 'member_id',
        'email', 'full_name', 'account_name', 'store_name'
    )


admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.Member, MemberAdmin)
