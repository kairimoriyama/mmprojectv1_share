from django.urls import path
from . import views


app_name = 'bankaccount'

urlpatterns = [
    path('list_all/', views.StatementList.as_view(), name='list_all'),
    path('correspondence_amount/', views.correspondence_amount, name='correspondence_amount'),
    path('detail_statement/', views.DetailStatement.as_view(), name='detail_statement'),
]