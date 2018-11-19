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
    TemplateSendMessage, ButtonsTemplate,
    MessageAction, ConfirmTemplate,
    URIAction,
)

from accounts.models import Account
from diagnoses.models import Diagnosis, Answer
from diagnoses.services import DiagnosisService


class LineChatbotService:
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

    def __init__(self):
        # NOTE: ミズノ用にホットモックで実装
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
        print(messages)
        self.api.reply_message(
            event.reply_token,
            messages,
        )

    def reply_follow_event(self, event):
        # NOTE: ミズ用にホットモックで実装
        # NOTE: 友達登録処理を追加
        FOLLOW_MESSAGES = [
            'MIZUNO BASEBALL ◯◯さん、友だち登録ありがとうございます(shiny)',
            'MIZUNO BASEBALL MIZUNO BASEBALLでは、野球を中心とした商品情報やおすすめ情報をお届けします(baseball)',
            'MIZUNO BASEBALL 「MENU」から〇〇さんにぴったりの商品を見つけよう(ok)',
        ]
        messages = [TextSendMessage(text=text_message) for text_message in FOLLOW_MESSAGES]
        self.reply_messages(event, messages)
        return messages

    def create_question_message(self, service, question):
        answers = service.get_related_answers(question)
        message = TemplateSendMessage(
            alt_text=str(question.question_id),
            template=ButtonsTemplate(
                # thumbnail_image_url=question.image,
                thumbnail_image_url=None,
                title=question.title,
                text=question.title,
                actions=[
                    MessageAction(
                        label=answer.title,
                        text=answer.title
                    )
                    for answer in answers
                ]
            )
        )
        return message

    def create_product_message(self, product):
        print(product.images[0])
        messages = [
            TextSendMessage(text='あなたへのおすすめ商品はこちらです'),
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url=product.images[0],
                    title=product.title,
                    text=product.title,
                    actions=[
                        URIAction(
                            label='詳細を見る',
                            uri=product.detail_url
                        ),
                        MessageAction(
                            label='カートに入れる',
                            text='未実装'
                        ),
                    ]
                )
            )
        ]
        return messages

    def reply_message_event(self, event):
        # 診断トリガーの場合
        # NOTE: ミズ用にホットモックで実装
        text = event.message.text
        account, created = Account.objects.get_or_create(name='mizuno')
        try:
            diagnosis = Diagnosis.objects.get(account=account, phase=text)
            service = DiagnosisService(account)
            messages = [TextSendMessage(text=message) for message in diagnosis.preface]
            # 最初の質問を作成
            first_question = diagnosis.first_question
            messages.append(self.create_question_message(service, first_question))
            self.reply_messages(event, messages)
            return messages
        except Diagnosis.DoesNotExist:
            pass
        # 診断回答の場合
        # NOTE: メッセージ履歴をログに残し、前回のメッセージが質問の場合に回答を返すように修正
        service = DiagnosisService(account)
        question = service.get_next_question(text)
        if question:
            messages = [self.create_question_message(service, question)]
            self.reply_messages(event, messages)
            return messages

        product = service.get_product(text)
        if product:
            messages = self.create_product_message(product)
            self.reply_messages(event, messages)
            return messages

        # messages = [TextSendMessage(text=event.message.text)]
        messages = []
        self.reply_messages(event, messages)
        return messages
