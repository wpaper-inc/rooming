from django.urls import path

from . import views


app_name = 'diagnoses'

urlpatterns = [
    path('mizuno/admin', views.MizunoAdminView.as_view(), name='admin'),
]
