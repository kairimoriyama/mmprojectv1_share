from django.urls import path
from . import views


app_name = 'procurement'

urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),

    path('list_request/', views.ListRequest.as_view(), name='list_request'),
    path('list_order/', views.ListOrder.as_view(), name='list_order'),

    path('detail_request/', views.DetailRequest.as_view(), name='detail_request'),
    path('detail_order/', views.DetailOrder.as_view(), name='detail_order'),

    path('create_request/', views.CreateRequest.as_view(), name='create_request'),
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),

    path('update_request/', views.UpdateRequest.as_view(), name='update_request'),
    path('update_order/', views.UpdateOrder.as_view(), name='update_order'),
]