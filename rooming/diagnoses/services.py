import io
import xlrd

from django.db import IntegrityError

from products.models import Product
from . import models


class DiagnosisService:
    DIAGNOSES_SHEET = 0
    PRODUCTS_SHEET = 1
    TYPES = {
        'カルーセル': models.Question.MESSAGE_TYPE_CAROUSEL,
        'クイックリプライ': models.Question.MESSAGE_TYPE_QUICK_REPLY,
        'ボタン': models.Question.MESSAGE_TYPE_BUTTON,
    }

    def __init__(self, account, *args, **kwargs):
        self.account = account

    def get_related_answers(self, question):
        qas = models.QuestionAnswer.objects.filter(question=question, account=self.account)
        answers = [qa.answer for qa in qas]
        return answers

    def get_next_question(self, answer_phase):
        qa = models.QuestionAnswer.objects.filter(answer__title=answer_phase,
                                               account=self.account).first()
        return qa and qa.next_question

    def get_product(self, answer_phase):
        try:
            qap = models.QuestionAnswerProduct.objects.get(answer__title=answer_phase)
        except models.QuestionAnswerProduct.DoesNotExist:
            return None
        return qap.product

    def get_next_question_or_product(self, answer_id):
        answer = models.Answer.objects.get(answer_id=answer_id)
        qa = models.QuestionAnswer.objects.filter(answer=answer, account=self.account).first()
        if qa and qa.next_question:
            return qa.next_question, None

        qap = models.QuestionAnswerProduct.objects.filter(answer=answer).first()
        if qap and qap.product:
            return None, qap.product

        return None, None

    def get_suggested_product(self, question, answer):
        try:
            qap = models.QuestionAnswerProduct.objects.get(
                question=question,
                answer=answer,
                account=self.account,
            )
        except models.QuestionAnswerProduct:
            return None
        return qap.product

    def get_message_type(self, type_str):
        return self.TYPES[type_str]

    def import_excel(self, filepath):
        # excep_file = io.TextIOWrapper(file)
        book = xlrd.open_workbook(filepath)

        # 質問一覧を作成
        question_sheet = book.sheet_by_index(self.DIAGNOSES_SHEET)
        products_sheet = book.sheet_by_index(self.PRODUCTS_SHEET)

        diagnoses = {}

        # 商品一覧を作成
        for rx in range(1, products_sheet.nrows):
            product_number = products_sheet.cell_value(rowx=rx, colx=0)
            removal_words = ['＋', '税', '¥', ',']
            price = products_sheet.cell_value(rowx=rx, colx=5)
            for w in removal_words:
                price = price.replace(w, '')
            price = int(price)
            product, created = Product.objects.get_or_create(
                account=self.account,
                detail_url=products_sheet.cell_value(rowx=rx, colx=1),
                title=products_sheet.cell_value(rowx=rx, colx=3),
                images=[products_sheet.cell_value(rowx=rx, colx=4)],
                price=price,
                tax_flag=False, # 税抜き
                model=products_sheet.cell_value(rowx=rx, colx=6),
                description=products_sheet.cell_value(rowx=rx, colx=7),
                external_id=product_number,
            )
            diagnoses[product_number] = product

        # 質問:回答のフォーマットに変換する
        first_question = None
        current_question_id = None
        answers = []

        for rx in range(1, question_sheet.nrows):
            # 質問を取得
            question_id = question_sheet.cell_value(rowx=rx, colx=0)
            question_type = question_sheet.cell_value(rowx=rx, colx=1)

            # 質問/回答の場合
            if question_type != '結果':
                # 新しい質問の場合
                if question_id != '':
                    # 質問の作成
                    current_question_id = question_id
                    message_type = self.get_message_type(question_type)
                    question, created = models.Question.objects.get_or_create(
                        title=question_sheet.cell_value(rowx=rx, colx=2),
                        image=None,
                        account=self.account,
                        message_type=message_type,
                        note1=question_id
                    )
                    diagnoses[question_id] = question
                    if not first_question:
                        first_question = question

                # 回答の作成
                next_diagnosis = question_sheet.cell_value(rowx=rx, colx=4)
                answer, created = models.Answer.objects.get_or_create(
                    title=question_sheet.cell_value(rowx=rx, colx=3),
                    image=None,
                    account=self.account,
                    note1=current_question_id
                )
                answers.append(dict(
                    obj=answer,
                    question_number=current_question_id,
                    next_number=question_sheet.cell_value(rowx=rx, colx=4),
                ))

        for answer in answers:
            question_number = answer['question_number']
            next_number = answer['next_number']
            answer = answer['obj']

            question = diagnoses[question_number]
            q_or_p = diagnoses[next_number]

            if type(q_or_p) == models.Question:
                qa, created = models.QuestionAnswer.objects.get_or_create(
                    question=question,
                    answer=answer,
                    next_question=q_or_p,
                    account=self.account,
                )
            else:
                try:
                    qa, created = models.QuestionAnswer.objects.get_or_create(
                        question=question,
                        answer=answer,
                        next_question=None,
                        account=self.account,
                    )
                    qap, created = models.QuestionAnswerProduct.objects.get_or_create(
                        question=question,
                        answer=answer,
                        product=q_or_p,
                    )
                except IntegrityError:
                    print(question.title)
                    print(answer.title)

        models.Diagnosis.objects.get_or_create(
            phase='診断',
            preface=[],
            first_question=first_question,
            account=self.account
        )
