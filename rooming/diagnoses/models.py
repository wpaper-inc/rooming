import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField

from lib.models import BaseModelMixin
from . import managers


class Question(BaseModelMixin):
    '''質問'''
    question_id = models.UUIDField(default=uuid.uuid4,
                                   unique=True,
                                   editable=False)
    title = models.TextField()

    objects = managers.QuestionManager()
    all_objects = managers.QuestionManager(include_soft_deleted=True)

    class Meta:
        db_table = 'question'
        verbose_name = 'Question/質問'
        verbose_name_plural = 'Questions/質問'
        indexes = [
            models.Index(fields=['question_id']),
        ]


class Answer(BaseModelMixin):
    '''回答'''
    answer_id = models.UUIDField(default=uuid.uuid4,
                                 unique=True,
                                 editable=False)
    title = models.TextField()

    objects = managers.AnswerManager()
    all_objects = managers.AnswerManager(include_soft_deleted=True)

    class Meta:
        db_table = 'answer'
        verbose_name = 'Answer/質問'
        verbose_name_plural = 'Answers/質問'
        indexes = [
            models.Index(fields=['answer_id']),
        ]


class QuestionAnswer(BaseModelMixin):
    '''質問回答回答'''
    question_answer_id = models.UUIDField(default=uuid.uuid4,
                                          unique=True,
                                          editable=False)
    question = models.ForeignKey('diagnoses.Question', on_delete=models.CASCADE)
    answer = models.ForeignKey('diagnoses.Answer', on_delete=models.CASCADE)

    objects = managers.QuestionAnswerManager()
    all_objects = managers.QuestionAnswerManager(include_soft_deleted=True)

    class Meta:
        db_table = 'question_answer'
        verbose_name = 'QuestionAnswer/質問回答回答'
        verbose_name_plural = 'QuestionAnswers/質問回答回答'
        unique_together = ('question', 'answer', 'live')
        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['answer']),
            models.Index(fields=['question', 'answer']),
        ]
