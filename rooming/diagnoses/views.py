import base64

from django.views.generic.base import View
from django.shortcuts import render
from django.utils.decorators import method_decorator

from basicauth.decorators import basic_auth_required

from users.models import Activity


@method_decorator(basic_auth_required, name='dispatch')
class MizunoAdminView(View):
    template = 'diagnoses/admin.html'
    def get(self, request):
        # 統計情報を取得
        aggregate = Activity.objects.aggregate()

        return render(request, self.template, aggregate)
