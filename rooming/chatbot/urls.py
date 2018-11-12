from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('line/webhook', views.LineChatbotView.as_view(), name='line'),
]
