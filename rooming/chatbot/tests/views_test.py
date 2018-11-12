import os
import json

from django.test import TestCase
from django.core import management

from rest_framework.test import APIRequestFactory
from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselTemplate,
)

from accounts.models import Member
from chatbot import views, services


class LineChatbotViewTest(TestCase):
    HTTP_SUCCESS = 200
    FOLLOW_FIRST_MESSAGES = 3
    USUAL_MESSAGES = 1

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
        self.service = services.LineChatbotService()

    def test_create_user(self):
        # 友達登録したユーザーは、DBに登録して挨拶文を送信する
        data = self.follow_account()
        request = self.factory.post('/line/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, self.HTTP_SUCCESS)
        # 挨拶文の送信
        reply_messages = self.service.direct_handle(data)
        self.assertEqual(len(reply_messages), self.FOLLOW_FIRST_MESSAGES)
        self.assertTrue(all(map(lambda m: type(m) == TextSendMessage, reply_messages)))

    def test_start_search_product(self):
        data = self.message_event('商品検索')
        request = self.factory.post('/line/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, self.HTTP_SUCCESS)
        # 検索結果のLINE返答
        reply_messages = self.service.direct_handle(data)
        self.assertEqual(len(reply_messages), self.USUAL_MESSAGES)
        message = reply_messages[0]
        # self.assertEqual(message, TemplateSendMessage)
        # self.assertEqual(message.template, CarouselTemplate)

    def test_diagnosis(self):
        data = self.message_event('動的フィッティング診断')
        request = self.factory.post('/line/', data)
        response = self.view(request)
        self.assertEqual(response.status_code, self.HTTP_SUCCESS)
        # 診断のLINE返答
        reply_messages = self.service.direct_handle(data)
        self.assertEqual(len(reply_messages), self.USUAL_MESSAGES)
        message = reply_messages[0]
