from django.urls import path
from .views import quick_info_home

urlpatterns = [
    path('', quick_info_home, name='quick_info_home'),
]