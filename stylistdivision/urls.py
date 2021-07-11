from django.urls import path
from . import views


app_name = 'stylistdivision'

urlpatterns = [
    path('list_project/', views.ListProject.as_view(), name='list_project'),
    path('list_settlement/', views.ListSettlement.as_view(), name='list_settlement'),
]