from django.urls import path
from .views import self_service_home

urlpatterns = [
    path('', self_service_home, name='self_service_home'),
]