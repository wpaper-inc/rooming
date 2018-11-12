from rest_framework.views import APIView
from rest_framework.response import Response

from . import services


class LineChatbotView(APIView):
    def post(self, request):
        service = services.LineChatbotService()
        service.callback(request)
        return Response()
