from django.urls import path
from . import views


app_name = 'procurement'

urlpatterns = [
    path('list_all/', views.ListALL.as_view(), name='list_all'),
    path('list_request/', views.ListRequest.as_view(), name='list_request'),
    path('list_order/', views.ListOrder.as_view(), name='list_order'),

    path('detail_request/<int:pk>', views.DetailRequest.as_view(), name='detail_request'),
    path('detail_order/<int:pk>', views.DetailOrder.as_view(), name='detail_order'),

    path('create_request/', views.CreateRequest.as_view(), name='create_request'),
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),

    path('update_request/<int:pk>', views.UpdateRequest.as_view(), name='update_request'),
    path('update_order/<int:pk>', views.UpdateOrder.as_view(), name='update_order'),
    path('update_request_order/<int:pk>', views.UpdateRequestToOrder.as_view(), name='update_request_order')
]