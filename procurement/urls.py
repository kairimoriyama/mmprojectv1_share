from django.urls import path
from . import views


app_name = 'procurement'

urlpatterns = [
    path('index/', views.ItemIndex.as_view(), name='index'),
]