import io
import json
import requests
from PIL import Image

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from accounts.services import TrackingURLService
from users.models import Activity
from . import services


@csrf_exempt
def line_chatbot(request, account_id):
    service = services.LineChatbotService()
    service.callback(request)
    return HttpResponse(json.dumps({}), content_type='application/json', status=200)


@csrf_exempt
def imagemap(request, account_id, product_id, size):
    url = 'https://s3-ap-northeast-1.amazonaws.com/rmng/assets/mizuno/diagnosis/%E8%A8%BA%E6%96%AD%E7%94%BB%E5%83%8F.jpg'
    res = requests.get(url, stream=True)
    image = Image.open(io.BytesIO(res.content))
    new_height = size
    height, width, channel = im.shape
    new_width  = new_height * width / height
    print(new_width)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    response = HttpResponse(content_type='image/jpeg', status=200)
    image.save(response, "JPEG")
    return response


@csrf_exempt
def redirect(request, tracking_url_id=None):
    service = TrackingURLService()
    url = service.reverse_link(tracking_url_id)
    print(url)
    if not url:
        raise Http404()
    return HttpResponseRedirect(url)
