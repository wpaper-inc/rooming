import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import services


@csrf_exempt
def line_chatbot(request):
    service = services.LineChatbotService()
    service.callback(request)
    return HttpResponse(json.dumps({}), content_type='application/json', status=200)
