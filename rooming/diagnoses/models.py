import uuid

from django.db import models
from django.contrib.postgres import fields
from django.contrib.postgres.fields import JSONField

from lib.models import BaseModelMixin
from . import managers


class Diagnosis(BaseModelMixin):
    '''企業の診断とトリガーとなる文言'''
    diagnosis_id = models.UUIDField(default=uuid.uuid4,
                                   unique=True,
                                   editable=False)
    phase = models.CharField(max_length=2000)
    preface = fields.ArrayField(models.CharField(max_length=2000), size=8)
    first_question = models.ForeignKey('diagnoses.Question', on_delete=models.CASCADE)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)

    objects = managers.DiagnosisManager()
    all_objects = managers.DiagnosisManager(include_soft_deleted=True)

    class Meta:
        db_table = 'diagnosis'
        verbose_name = 'Diagnosis/診断'
        verbose_name_plural = 'Diagnoses/診断'
        indexes = [
            models.Index(fields=['diagnosis_id']),
            models.Index(fields=['phase']),
            models.Index(fields=['first_question']),
            models.Index(fields=['account']),
            models.Index(fields=['phase', 'account']),
        ]


class Question(BaseModelMixin):
    '''質問'''
    question_id = models.UUIDField(default=uuid.uuid4,
                                   unique=True,
                                   editable=False)
    title = models.TextField()
    image = models.URLField(null=True, default=None, blank=True)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, null=True, default=None)

    objects = managers.QuestionManager()
    all_objects = managers.QuestionManager(include_soft_deleted=True)

    class Meta:
        db_table = 'question'
        verbose_name = 'Question/質問'
        verbose_name_plural = 'Questions/質問'
        indexes = [
            models.Index(fields=['question_id']),
            models.Index(fields=['account']),
        ]


class Answer(BaseModelMixin):
    '''回答'''
    answer_id = models.UUIDField(default=uuid.uuid4,
                                 unique=True,
                                 editable=False)
    title = models.TextField()
    image = models.URLField(null=True, default=None, blank=True)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, null=True, default=None)

    objects = managers.AnswerManager()
    all_objects = managers.AnswerManager(include_soft_deleted=True)

    class Meta:
        db_table = 'answer'
        verbose_name = 'Answer/質問'
        verbose_name_plural = 'Answers/質問'
        indexes = [
            models.Index(fields=['answer_id']),
            models.Index(fields=['account']),
        ]


class QuestionAnswer(BaseModelMixin):
    '''質問回答回答'''
    question_answer_id = models.UUIDField(default=uuid.uuid4,
                                          unique=True,
                                          editable=False)
    question = models.ForeignKey('diagnoses.Question',
                                 related_name='question',
                                 on_delete=models.CASCADE)
    answer = models.ForeignKey('diagnoses.Answer', on_delete=models.CASCADE)
    next_question = models.ForeignKey('diagnoses.Question',
                                      related_name='next_question',
                                      on_delete=models.CASCADE,
                                      null=True, default=None,
                                      blank=True)
    account = models.ForeignKey('accounts.Account',
                                on_delete=models.CASCADE,
                                null=True,
                                default=None,
                                blank=True)

    objects = managers.QuestionAnswerManager()
    all_objects = managers.QuestionAnswerManager(include_soft_deleted=True)

    class Meta:
        db_table = 'question_answer'
        verbose_name = 'QuestionAnswer/質問回答関連'
        verbose_name_plural = 'QuestionAnswers/質問回答関連'
        unique_together = ('question', 'answer', 'live')
        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['answer']),
            models.Index(fields=['account']),
            models.Index(fields=['question', 'answer']),
        ]

class QuestionAnswerProduct(BaseModelMixin):
    qap_id = models.UUIDField(default=uuid.uuid4,
                              unique=True,
                              editable=False)
    question = models.ForeignKey('diagnoses.Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('diagnoses.Answer', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    objects = managers.QuestionAnswerProductManager()
    all_objects = managers.QuestionAnswerProductManager(include_soft_deleted=True)

    class Meta:
        db_table = 'question_answer_product'
        verbose_name = 'QuestionAnswerProduct/質問回答商品関連'
        verbose_name_plural = 'QuestionAnswerProducts/質問回答商品関連'
        unique_together = ('question', 'answer', 'live')
        indexes = [
            models.Index(fields=['question', 'answer']),
        ]
