from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('line/webhook', views.line_chatbot, name='line'),
]
