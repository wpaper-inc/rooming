from django.urls import path

from . import views

app_name = 'chatbot'

urlpatterns = [
    path('line/<slug:account_id>/webhook', views.line_chatbot, name='line'),
    path('line/<slug:account_id>/imagemap/<slug:product_id>/<int:size>', views.imagemap, name='line_imagemap'),
    path('r/<slug:tracking_url_id>', views.redirect, name='redirect'),
]
