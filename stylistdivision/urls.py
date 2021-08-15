from django.urls import path
from . import views


app_name = 'stylistdivision'

urlpatterns = [
    path('list_project/', views.ListProject.as_view(), name='list_project'),
    path('detail_project/<int:pk>', views.DetailProject.as_view(), name='detail_project'),
    path('create_project/', views.CreateProject.as_view(), name='create_project'),
    path('update_project/<int:pk>', views.UpdateProject.as_view(), name='update_project'),

    path('list_client/', views.ListClient.as_view(), name='list_client'),
    path('detail_client/', views.DetailClient.as_view(), name='detail_client'),
    path('create_client/', views.CreateClient.as_view(), name='create_client'),
    path('update_client/', views.UpdateClient.as_view(), name='update_client'),


    path('list_settlement/', views.ListSettlement.as_view(), name='list_settlement'),
]