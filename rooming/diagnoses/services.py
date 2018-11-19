import io
import xlrd

from products.models import Product
from . import models


class DiagnosisService:
    def __init__(self, account, *args, **kwargs):
        self.account = account

    def get_related_answers(self, question):
        qas = models.QuestionAnswer.objects.filter(question=question, account=self.account)
        answers = [qa.answer for qa in qas]
        return answers

    def get_next_question(self, answer_phase):
        try:
            qa = models.QuestionAnswer.objects.get(answer__title=answer_phase,
                                                   account=self.account)
        except models.QuestionAnswer.DoesNotExist:
            return None
        return qa.next_question

    def get_product(self, answer_phase):
        try:
            qap = models.QuestionAnswerProduct.objects.get(answer__title=answer_phase)
        except models.QuestionAnswerProduct.DoesNotExist:
            return None
        return qap.product

    # def get_next_question(self, question, answer):
    #     try:
    #         qa = models.QuestionAnswers.objects.get(question=question,
    #                                                 answer=answer,
    #                                                 account=self.account)
    #     except models.QuestionAnswer.DoesNotExist:
    #         return None
    #     return qa.next_question

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

    def import_excel(self, filepath):
        # excep_file = io.TextIOWrapper(file)
        book = xlrd.open_workbook(filepath)

        # 質問一覧を作成
        question_sheet = book.sheet_by_index(0)
        first_question = None
        questions = {}
        for rx in range(1, question_sheet.nrows):
            question_id = question_sheet.cell_value(rowx=rx, colx=0)
            title = question_sheet.cell_value(rowx=rx, colx=1)
            image_url = question_sheet.cell_value(rowx=rx, colx=2)
            is_first_question = question_sheet.cell_value(rowx=rx, colx=3)
            question, created = models.Question.objects.get_or_create(
                title=title,
                image=image_url,
                account=self.account,
            )
            if is_first_question == 'y':
                first_question = question
            questions[title] = question

        # 回答一覧を作成
        answer_sheet = book.sheet_by_index(1)
        answers = {}
        for rx in range(1, answer_sheet.nrows):
            answer_id = answer_sheet.cell_value(rowx=rx, colx=0)
            title = answer_sheet.cell_value(rowx=rx, colx=1)
            image_url = None
            answer, created = models.Answer.objects.get_or_create(
                title=title,
                image=image_url,
                account=self.account,
            )
            answers[title] = answer

        # 商品一覧を取得
        product_sheet = book.sheet_by_index(2)
        products = {}
        for rx in range(1, product_sheet.nrows):
            product_id = product_sheet.cell_value(rowx=rx, colx=2)
            try:
                product = Product.objects.get(external_id=product_id)
            except Product.DoesNotExist:
                name = product_sheet.cell_value(rowx=rx, colx=1)
                image = product_sheet.cell_value(rowx=rx, colx=3)
                description = product_sheet.cell_value(rowx=rx, colx=4)
                detail_url = product_sheet.cell_value(rowx=rx, colx=5)
                product = Product.objects.create(
                    title=name,
                    description=description,
                    images=[image],
                    detail_url=detail_url,
                    external_id=product_id,
                    account=self.account,
                )
            products[product_id] = product

        # 質問回答関連を作成
        qa_sheet = book.sheet_by_index(3)
        for rx in range(1, qa_sheet.nrows):
            question_idx = qa_sheet.cell_value(rowx=rx, colx=0)
            question = questions[question_idx]
            answer_idx = qa_sheet.cell_value(rowx=rx, colx=1)
            answer = answers[answer_idx]
            next_q_idx = qa_sheet.cell_value(rowx=rx, colx=2)
            next_question = questions.get(question_idx, None)
            product_id = qa_sheet.cell_value(rowx=rx, colx=4)
            product = products.get(product_id, None)
            models.QuestionAnswer.objects.get_or_create(
                question=question,
                answer=answer,
                next_question=next_question,
                account=self.account,
            )
            if product:
                models.QuestionAnswerProduct.objects.get_or_create(
                    question=question,
                    answer=answer,
                    product=product,
                )

        # 診断を作成
        diagnosis_sheet = book.sheet_by_index(4)
        phase = product_sheet.cell_value(rowx=1, colx=0)
        messages = []
        for i in range(1, 6):
            message = product_sheet.cell_value(rowx=1, colx=i)
            if message:
                messages.append(message)
        models.Diagnosis.objects.get_or_create(
            phase=phase,
            preface=messages,
            first_question=first_question,
            account=self.account,
        )
