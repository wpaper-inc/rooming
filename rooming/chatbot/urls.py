from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('line/<slug:account_id>/webhook', views.line_chatbot, name='line'),
]
