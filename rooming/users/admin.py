from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id',
        'line_user_id', 'full_name',
    )

class AccountUserAdmin(admin.ModelAdmin):
    def user_full_name(self, obj):
        if obj.user:
            return obj.user.full_name
        return ''
    user_full_name.short_description = 'user'
    def account_name(self, obj):
        if obj.account:
            return obj.account.name
        return ''
    account_name.short_description = 'account'
    list_display = (
        'account_user_id',
        'user_full_name', 'account_name',
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.AccountUser, AccountUserAdmin)
