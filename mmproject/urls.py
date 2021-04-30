from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import settings_common, dev

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # path('admin/', admin.site.urls),
    path('p-admin/', admin.site.urls),
    path('accounts/inactive/', TemplateView.as_view(template_name = 'inactive.html'), name='inactive'),  
    path('accounts/', include('allauth.urls')),
    path('goodidea/', include('goodidea.urls')),

    # 開発サーバーでメディアを配信できるようにする設定
]+ static( settings_common.MEDIA_URL, document_root = dev.MEDIA_ROOT )