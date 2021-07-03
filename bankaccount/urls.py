from django.urls import path
from . import views


app_name = 'bankaccount'

urlpatterns = [
    path('list_all/', views.StatementList.as_view(), name='list_all'),
    path('detail_statement/', views.DetailStatement.as_view(), name='detail_statement'),
]