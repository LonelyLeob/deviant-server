from django.urls import path
from .views import set_utm

urlpatterns = [
    path('', set_utm)
]