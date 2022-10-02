from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.DATA_URL, document_root=settings.DATA_ROOT)
    urlpatterns += static(settings.DRACO_URL, document_root=settings.DRACO_ROOT)
    urlpatterns += static(settings.FLATICON_URL, document_root=settings.FLATICON_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.IMG_URL, document_root=settings.IMG_ROOT)
    urlpatterns += static(settings.MODEL_URL, document_root=settings.MODEL_ROOT)
    urlpatterns += static(settings.FONT_URL, document_root=settings.FONT_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)