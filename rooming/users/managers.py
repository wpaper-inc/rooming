from livefield import LiveManager


class UserManager(LiveManager):
    pass

class ActivityManager(LiveManager):
    def get_ratio(self, devee, dever, floating=2):
        if dever == 0:
            return 0.0;
        result = devee / dever * 100
        return round(result, floating)

    def create_request_log(self, request):
        user = request.user
        path = request.path
        params = request.data
        instance = self.model.objects.create(user=user, path=path, params=params)
        return instance

    def aggregate(self):
        # 全体統計
        overview = dict()
        # 友達登録数
        from users.models import User
        overview['friends_count'] = User.objects.all().count()
        # 診断実行回数
        overview['diagnoses_count'] = self.filter(action='get_diagnoses').count()
        # 診断を実行した人数
        overview['members_count'] = self.filter(action='get_diagnoses').distinct('user_id').count()
        # 診断を実行した人数 / 友達登録数
        overview['members_per_friends'] = self.get_ratio(overview['members_count'], overview['friends_count'])

        # 回答状況に関する統計
        from diagnoses.models import Answer, QuestionAnswer
        questions = dict()
        # 全設問に対して集計
        for answer in Answer.objects.all():
            query = dict(
                params__events__0__type='postback',
                params__events__0__postback__data='action=answer&answer_id={}'.format(answer.answer_id)
            )
            answer_count = self.filter(**query).count()
            question = QuestionAnswer.objects.get(answer=answer).question

            if not questions.get(question.question_id):
                questions[question.question_id] = dict(question=question)
                questions[question.question_id]['answers'] = []
            questions[question.question_id]['answers'].append(dict(answer=answer, count=answer_count))
        # 回答に対して割合を算出
        for question_id, question in questions.items():
            answers_count = sum([a['count'] for a in question['answers']])
            questions[question_id]['answers_count'] = answers_count
            for answer in question['answers']:
                answer['ratio'] = self.get_ratio(answer['count'], answers_count)

        # 各診断結果に関する統計
        from products.models import Product
        from diagnoses.models import QuestionAnswerProduct
        from accounts.models import TrackingURL
        from django.db.models import Sum
        products = dict()
        for product in Product.objects.all():
            qap_querysets = QuestionAnswerProduct.objects.filter(product=product)
            product_count = 0
            for qap in qap_querysets:
                answer = qap.answer
                query = dict(
                    action='get_product',
                    params__events__0__type='postback',
                    params__events__0__postback__data='action=answer&answer_id={}'.format(answer.answer_id)
                )
                product_count += self.filter(**query).count()
            # 詳細はこちらを押した回数
            detail_count = TrackingURL.objects.filter(url=product.detail_url) \
                                              .aggregate(Sum('click_count')) \
                                              .get('click_count__sum')
            # キャンペーン参加を押した回数
            query = dict(
                action = 'get_campaign',
                params__events__0__type='postback',
                params__events__0__postback__data="action=campaign&product_id={}".format(product.product_id)
            )
            campaign_count = self.filter(**query).count()
            products[product] = dict(
                count=product_count,
                detail_count=detail_count,
                campaign_count=campaign_count,
            )
        # 割合を算出
        products_count = sum([values['count'] for p, values in products.items()])
        for product, values in products.items():
            values['ratio'] = self.get_ratio(values['count'], products_count)
            values['detail_ratio'] = self.get_ratio(values['detail_count'], values['count'])
            values['campaign_ratio'] = self.get_ratio(values['campaign_count'], values['count'])

        # 診断結果の全体統計
        overview['products_count'] = products_count
        overview['products_per_diagnoses'] = self.get_ratio(products_count, overview['diagnoses_count'])
        # 詳細を表示した「人数」
        detail_members = TrackingURL.objects.filter(url=product.detail_url) \
                                            .distinct('user_id') \
                                            .count()
        # キャンペーン参加を押した「人数」
        query = dict(
            action = 'get_campaign',
            params__events__0__type='postback',
        )
        campaign_members = self.filter(**query).distinct('user_id').count()
        overview['detail_count'] = detail_members
        overview['detail_per_member'] = self.get_ratio(detail_members, overview['members_count'])
        overview['campaign_count'] = campaign_members
        overview['campaign_per_member'] = self.get_ratio(campaign_members, overview['members_count'])
        return dict(overview=overview, questions=questions, products=products)

class AccountUserManager(LiveManager):
    pass
