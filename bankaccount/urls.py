from django.urls import path
from . import views


app_name = 'bankaccount'

urlpatterns = [
    path('list_all/', views.StatementList.as_view(), name='list_all'),
]