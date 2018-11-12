import os
import json

from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent,
    TextMessage, TextSendMessage,
)


class LineChatbotService:
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

    def __init__(self):
        print(self.LINE_CHANNEL_ACCESS_TOKEN)
        print(self.LINE_CHANNEL_SECRET)
        self.api = LineBotApi(self.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(self.LINE_CHANNEL_SECRET)
        self.mock = False
        self.handler.add(MessageEvent, message=TextMessage)(self.reply_message_event)
        self.handler.add(FollowEvent, message=TextMessage)(self.reply_follow_event)

    def direct_handle(self, body):
        self.mock = True
        parser = WebhookParser(self.LINE_CHANNEL_SECRET)
        parser.signature_validator.validate = lambda a, b: True # mock
        events = parser.parse(json.dumps(body), self.LINE_CHANNEL_SECRET)
        event = events[0]
        if type(event) == MessageEvent:
            return self.reply_message_event(event)
        elif type(event) == FollowEvent:
            return self.reply_follow_event(event)

    def callback(self, request):
        self.mock = False
        signature = request.META.get('HTTP_X_LINE_SIGNATURE')
        body = request.body.decode('utf-8')
        self.handler.handle(body, signature)

    def reply_messages(self, event, messages):
        if self.mock:
            return
        for message in messages:
            self.api.reply_message(
                event.reply_token,
                message
            )

    def reply_follow_event(self, event):
        FOLLOW_MESSAGES = [
            'MIZUNO BASEBALL ◯◯さん、友だち登録ありがとうございます(shiny)',
            'MIZUNO BASEBALL MIZUNO BASEBALLでは、野球を中心とした商品情報やおすすめ情報をお届けします(baseball)',
            'MIZUNO BASEBALL 「MENU」から〇〇さんにぴったりの商品を見つけよう(ok)',
        ]
        messages = [TextSendMessage(text=text_message) for text_message in FOLLOW_MESSAGES]
        self.reply_messages(event, messages)
        return messages

    def reply_message_event(self, event):
        messages = [TextSendMessage(text=event.message.text)]
        self.reply_messages(event, messages)
        return messages
