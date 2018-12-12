import os
import json
import urllib

from django.db.models import Q

from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent,
    TextMessage, TextSendMessage,
    PostbackEvent,
    ImageSendMessage, ImagemapSendMessage, BaseSize,
    TemplateSendMessage, ButtonsTemplate,
    CarouselTemplate, CarouselColumn,
    MessageAction, ConfirmTemplate,
    URIAction, PostbackAction,
    QuickReply, QuickReplyButton,
)

from accounts.models import Account, TrackingURL
from accounts.services import TrackingURLService
from products.models import Product
from diagnoses.models import Diagnosis, Answer
from diagnoses.services import DiagnosisService
from users.models import User, Activity, AccountUser


class LineChatbotService:
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

    def __init__(self):
        # NOTE: ミズノ用にホットモックで実装
        self.api = LineBotApi(self.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(self.LINE_CHANNEL_SECRET)
        self.mock = False
        self.request = None
        self.handler.add(MessageEvent, message=TextMessage)(self.reply_message_event)
        self.handler.default()(self.reply_event)

    def login_user(self, event, account):
        user_id = event.source.user_id
        user, created = User.objects.get_or_create(line_user_id=user_id)
        account_user, created = AccountUser.objects.get_or_create(user=user, account=account)
        return user

    def direct_handle(self, body):
        self.mock = True
        parser = WebhookParser(self.LINE_CHANNEL_SECRET)
        parser.signature_validator.validate = lambda a, b: True # mock
        events = parser.parse(json.dumps(body), self.LINE_CHANNEL_SECRET)
        event = events[0]
        if type(event) == MessageEvent:
            return self.reply_message_event(event)
        else:
            return self.reply_event(event)

    def callback(self, request):
        self.mock = False
        self.request = request
        signature = request.META.get('HTTP_X_LINE_SIGNATURE')
        body = request.body.decode('utf-8')
        self.body = json.loads(body)
        self.handler.handle(body, signature)

    def reply_messages(self, event, messages):
        if self.mock:
            return
        if len(messages) == 0:
            return
        self.api.reply_message(
            event.reply_token,
            messages,
        )

    def reply_follow_event(self, event):
        # NOTE: ミズ用にホットモックで実装
        # NOTE: 友達登録処理を追加
        pass
        # FOLLOW_MESSAGES = [
        #     'MIZUNO BASEBALL ◯◯さん、友だち登録ありがとうございます(shiny)',
        #     'MIZUNO BASEBALL MIZUNO BASEBALLでは、野球を中心とした商品情報やおすすめ情報をお届けします(baseball)',
        #     'MIZUNO BASEBALL 「MENU」から〇〇さんにぴったりの商品を見つけよう(ok)',
        # ]
        # messages = [TextSendMessage(text=text_message) for text_message in FOLLOW_MESSAGES]
        # self.reply_messages(event, messages)
        # return messages

    def reply_event(self, event):
        account, created = Account.objects.get_or_create(name='mizuno')
        user = self.login_user(event, account)

        if type(event) == PostbackEvent:
            data = urllib.parse.parse_qs(event.postback.data)
            action = data.get('action')[0]
            if action == 'campaign':
                product_id = data.get('product_id')[0]
                product = Product.objects.get(product_id=product_id)
                image = product.images[1]
                messages = [
                    ImageSendMessage(
                        original_content_url=image,
                        preview_image_url=image
                    ),
                    TextMessage(
                        text='🎁キャンペーン参加方法🎁\n①診断結果画像をダウンロード\n②TwitterかInstagramで、ハッシュタグ「#動的フィッティング」をつけて診断結果画像を投稿\n③MIZUNOオフィシャルアカウントをフォロー'
                    ),
                    TextMessage(
                        text='⚾️MIZUNOオフィシャルアカウント⚾️\n\n＜Twitter＞\nhttps://twitter.com/mizunopro_jp\n\n＜Instagram＞\nhttps://www.instagram.com/mizunobaseball_jp/'
                    ),
                    TextMessage(
                        text='🎉当選発表🎉\n\n参加者の中から抽選で10名様に、投稿した診断結果の商品をプレゼント❗️当選者にはMIZUNOオフィシャルアカウントからDMでご連絡いたします。'
                    )
                ]
                # ログを作成
                Activity.objects.create(
                    user=user,
                    path='/bot/line/mizuno/webhook',
                    account=account,
                    action='get_campaign',
                    action_id=product.product_id,
                    params=self.body
                )
                self.reply_messages(event, messages)
            elif action == 'answer':
                answer_id = data.get('answer_id')[0]
                service = DiagnosisService(account)
                question, product = service.get_next_question_or_product(answer_id)
                if question:
                    messages = [self.create_question_message(service, question)]
                    self.reply_messages(event, messages)
                    # ログを作成
                    Activity.objects.create(
                        user=user,
                        path='/bot/line/mizuno/webhook',
                        account=account,
                        action='get_question',
                        action_id=answer_id,
                        params=self.body
                    )
                    return messages
                elif product:
                    messages = self.create_product_message(product, account, user)
                    self.reply_messages(event, messages)
                    # ログを作成
                    Activity.objects.create(
                        user=user,
                        path='/bot/line/mizuno/webhook',
                        account=account,
                        action='get_product',
                        action_id=product.product_id,
                        params=self.body
                    )
                    return messages

    def create_question_message(self, service, question):
        answers = service.get_related_answers(question)
        if question.message_type == question.MESSAGE_TYPE_BUTTON:
            message = TemplateSendMessage(
                alt_text=question.title,
                template=ButtonsTemplate(
                    thumbnail_image_url=None,
                    text=question.title,
                    actions=[
                        PostbackAction(
                            label=answer.title,
                            data='action=answer&answer_id={}'.format(answer.answer_id)
                        )
                        for answer in answers
                    ]
                )
            )
        elif question.message_type == question.MESSAGE_TYPE_CAROUSEL:
            message = TemplateSendMessage(
                alt_text=question.title,
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url=None,
                            text=question.title,
                            actions=[
                                PostbackAction(
                                    label=answer.title,
                                    data='action=answer&answer_id={}'.format(answer.answer_id)
                                ),
                            ]
                        )
                        for answer in answers
                    ]
                )
            )
        elif question.message_type == question.MESSAGE_TYPE_QUICK_REPLY:
            message = TextSendMessage(text=question.title,
                                      quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=PostbackAction(
                                            label=answer.title,
                                            data='action=answer&answer_id={}'.format(answer.answer_id)
                                        ))
                                      for answer in answers]))
        return message

    def create_product_message(self, product, account, user):
        description = product.description + '(￥{:,}＋税)'.format(product.price)
        t_service = TrackingURLService()
        link = t_service.generate_link(
            account, user, product.detail_url, self.request)

        messages = [
            TextSendMessage(text='動的フィティング診断終了👍👍あなたにぴったりのシューズはこちら❗️❗'),
            TemplateSendMessage(
                alt_text=product.description,
                template=ButtonsTemplate(
                    thumbnail_image_url=product.images[0],
                    title=product.title,
                    text=description,
                    actions=[
                        URIAction(
                            label='詳細はこちら',
                            uri=link
                        ),
                        PostbackAction(
                            label='キャンペーンに参加',
                            data='action=campaign&product_id={}'.format(product.product_id)
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
        user = self.login_user(event, account)
        try:
            query = Q(phase1=text) | Q(phase2=text) | Q(phase3=text) & Q(account=account)
            diagnosis = Diagnosis.objects.filter(query).first()
            service = DiagnosisService(account)
            # MIZUNO用ホットモック
            base_url = self.request.build_absolute_uri('/bot/line/mizuno/imagemap/dummy')
            base_url = base_url.replace('http', 'https')
            messages = [
                ImagemapSendMessage(
                    base_url=base_url,
                    alt_text='診断',
                    base_size=BaseSize(height=1300, width=1040),
                    actions=[]
                )
            ]
            # messages = [
            #     ImageSendMessage(
            #         original_content_url='https://s3-ap-northeast-1.amazonaws.com/rmng/assets/mizuno/%E8%A8%BA%E6%96%AD%E9%96%8B%E5%A7%8B%E6%99%82.jpg',
            #         preview_image_url='https://s3-ap-northeast-1.amazonaws.com/rmng/assets/mizuno/%E8%A8%BA%E6%96%AD%E9%96%8B%E5%A7%8B%E6%99%82.jpg'
            #     )
            # ]
            # messages = [TextSendMessage(text=message) for message in diagnosis.preface]
            # 最初の質問を作成
            first_question = diagnosis.first_question
            messages.append(self.create_question_message(service, first_question))
            self.reply_messages(event, messages)

            # ログを作成
            Activity.objects.create(
                user=user,
                path='/bot/line/mizuno/webhook',
                account=account,
                action='get_diagnoses',
                params=self.body
            )

            return messages
        except Diagnosis.DoesNotExist:
            pass

        # messages = [TextSendMessage(text=event.message.text)]
        messages = []
        self.reply_messages(event, messages)
        return messages
