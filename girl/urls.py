from django.urls import path
from .views import GirlAPIView

urlpatterns = [
    path('<str:slug>', GirlAPIView.as_view())
]
