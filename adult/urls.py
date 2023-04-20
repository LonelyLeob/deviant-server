from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import MEDIA_ROOT, STATIC_ROOT, DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('girls/', include('girl.urls')),
]

if DEBUG:
    urlpatterns += static("media/", document_root=MEDIA_ROOT)
    urlpatterns += static("media/", document_root=STATIC_ROOT)