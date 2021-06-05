from django.urls import path
from . import views


app_name = 'staffdb'

urlpatterns = [
    path('staff_all/', views.ListALL.as_view(), name='staff_all'),
]