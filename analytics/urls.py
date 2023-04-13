from django.urls import path
from .views import set_utm_and_redirect

urlpatterns = [
    path('', set_utm_and_redirect)
]