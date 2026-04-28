from django.urls import path
from . import views

urlpatterns = [

    path('', views.swipe_home, name='swipe_home'),

    # Apply
    path('apply/', views.swipe_apply, name='swipe_apply'),


    # Details
    path('details/', views.view_swipe_details, name='view_swipe_details'),

    # Filters
    path('pending/', views.recent_swipe, name='recent_swipe'),
    path('approved/', views.approve_swipe, name='approve_swipe'),
    path('rejected/', views.reject_swipe, name='reject_swipe'),
    path('lapsed/', views.lapsed_swipe, name='lapsed_swipe'),
]