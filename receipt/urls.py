from django.urls import path
from . import views


app_name = 'receipt'

urlpatterns = [
    path('index/', views.ItemIndex.as_view(), name='index'),
]