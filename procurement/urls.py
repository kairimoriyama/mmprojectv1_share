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
    path('create_order_request/', views.CreateOrderAndRequest.as_view(), name='create_order_request'),

    path('update_request/<int:pk>', views.UpdateRequest.as_view(), name='update_request'),
    path('update_order/<int:pk>', views.UpdateOrder.as_view(), name='update_order'),

    # ajax
    path('ajax_get_requestStaff/', views.ajax_get_requestStaff, name='ajax_get_requestStaff'),
    path('ajax_get_adminStaff/', views.ajax_get_adminStaff, name='ajax_get_adminStaff'),
    path('ajax_get_orderStaff/', views.ajax_get_orderStaff, name='ajax_get_orderStaff'),
    path('ajax_get_acceptanceStaff/', views.ajax_get_acceptanceStaff, name='ajax_get_acceptanceStaff'),
    path('ajax_get_requestStaff_filter/', views.ajax_get_requestStaff_filter, name='ajax_get_requestStaff_filter'),

]