import os
import json

from django.test import TestCase
from django.core import management

from diagnoses.models import Question, Answer, QuestionAnswer


class LineChatbotViewTest(TestCase):
    def setUp(self):
        management.call_command('initialize_app')

        self.account = Member.objects.get(email=os.getenv('SUPER_MEMBER_EMAIL')).account
