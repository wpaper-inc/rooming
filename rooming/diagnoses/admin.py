from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class DiagnosisAdmin(admin.ModelAdmin):
    def account_name(self, obj):
        if obj.account:
            return obj.account.name
        return ''
    account_name.description = 'account'
    list_display = (
        'diagnosis_id', 'phase',
        'preface', 'first_question',
        'account_name',
    )


class QuestionAdmin(admin.ModelAdmin):
    def account_name(self, obj):
        if obj.account:
            return obj.account.name
        return ''
    account_name.description = 'account'
    list_display = (
        'question_id', 'title',
        'image', 'account_name',
    )


class AnswerAdmin(admin.ModelAdmin):
    def account_name(self, obj):
        if obj.account:
            return obj.account.name
        return ''
    account_name.description = 'account'
    list_display = (
        'answer_id', 'title',
        'image', 'account_name',
    )


class QuestionAnswerAdmin(admin.ModelAdmin):
    def account_name(self, obj):
        if obj.account:
            return obj.account.name
        return ''
    account_name.description = 'account'
    list_display = (
        'question_answer_id', 'question',
        'answer', 'next_question', 'account_name',
    )


class QuestionAnswerProductAdmin(admin.ModelAdmin):
    list_display = (
        'qap_id', 'question',
        'answer', 'product',
    )


admin.site.register(models.Diagnosis, DiagnosisAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(models.QuestionAnswerProduct, QuestionAnswerProductAdmin)
