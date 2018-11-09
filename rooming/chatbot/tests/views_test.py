import os
import json

from django.test import TestCase
from django.core import management

from rest_framework.test import APIRequestFactory

from accounts.models import Member
from chatbot import views


class LineChatbotViewTest(TestCase):
    def message_event(self, text):
        file_dir = os.path.dirname(__file__)
        webhook_sample_json_path = os.path.join(file_dir, 'webhook.json')
        with open(webhook_sample_json_path, 'rb') as fp:
            body = json.loads(fp.read())
        events = {'events': [body['events'][0]]}
        events['events'][0]['message']['text'] = text
        return events

    def follow_account(self):
        file_dir = os.path.dirname(__file__)
        webhook_sample_json_path = os.path.join(file_dir, 'webhook.json')
        with open(webhook_sample_json_path, 'rb') as fp:
            body = json.loads(fp.read())
        events = {'events': [body['events'][1]]}
        return events

    def setUp(self):
        # Every test needs a client.
        management.call_command('initialize_app')

        self.account = Member.objects.get(email=os.getenv('SUPER_MEMBER_EMAIL')).account
        self.factory = APIRequestFactory()
        self.view = views.LineChatbotView.as_view()

    def test_create_user(self):
        # 友達登録したユーザーは、DBに登録して挨拶文を送信する
        data = self.follow_account()
        request = self.factory.post('/line/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_start_search_product(self):
        data = self.message_event('商品検索')
        request = self.factory.post('/line/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_diagnosis(self):
        data = self.message_event('動的フィッティング診断')
        request = self.factory.post('/line/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
