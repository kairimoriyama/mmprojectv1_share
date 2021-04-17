from django.urls import path
from . import views


app_name = 'goodidea'

urlpatterns = [
    path('list_all/', views.ItemListALL.as_view(), name='list_all'),
<<<<<<< HEAD
    path('list_due/', views.ItemListDue.as_view(), name='list_due'),
    path('list_idea/', views.ItemListIdea.as_view(), name='list_idea'),
    path('list_action/', views.ItemListAction.as_view(), name='list_action'),
    path('list_filter/', views.ItemListFilter.as_view(), name='list_filter'),

    path('export/', views.item_export, name='item_export'),

    path('detail_item/<int:pk>', views.ItemDetail.as_view(), name='detail_item'),
    path('detail_sub/<int:pk>', views.ItemDetailSub.as_view(), name='detail_sub'),
    path('detail_filter/<int:pk>', views.ItemDetailFilter.as_view(), name='detail_filter'),
    path('detail_due/<int:pk>', views.ItemDetailSub.as_view(), name='detail_due'),


    path('create_idea/', views.ItemCreateIdea.as_view(), name='create_idea'),
    path('create_action/', views.ItemCreateAction.as_view(), name='create_action'),
    
    path('update_item/<int:pk>', views.ItemUpdate.as_view(), name='update_item'),
    path('update_filter/<int:pk>', views.ItemUpdateFilter.as_view(), name='update_filter'),
    path('update_sub/<int:pk>', views.ItemUpdateSub.as_view(), name='update_sub'),

=======
    path('export/', views.item_export, name='item_export'),
    path('list_idea/', views.ItemListIdea.as_view(), name='list_idea'),
    path('list_action/', views.ItemListAction.as_view(), name='list_action'),
    path('list_filter/', views.ItemListFilter.as_view(), name='list_filter'),
    path('detail_item/<int:pk>', views.ItemDetail.as_view(), name='detail_item'),
    path('detail_sub/<int:pk>', views.ItemDetailSub.as_view(), name='detail_sub'),
    path('detail_filter/<int:pk>', views.ItemDetailFilter.as_view(), name='detail_filter'),
    path('create_idea/', views.ItemCreateIdea.as_view(), name='create_idea'),
    path('create_action/', views.ItemCreateAction.as_view(), name='create_action'),
    path('update_item/<int:pk>', views.ItemUpdate.as_view(), name='update_item'),
    path('update_filter/<int:pk>', views.ItemUpdateFilter.as_view(), name='update_filter'),
>>>>>>> origin/main
]