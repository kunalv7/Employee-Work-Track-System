from django.urls import path
from . import views

urlpatterns = [

    path('leave_home/', views.leave_home, name='leave_home'),
    path('leave_apply/', views.leave_apply, name='leave_apply'),

    # USER
    path('recent_leave/', views.recent_leave, name='recent_leave'),
    path('approve_leave/', views.approve_leave, name='approve_leave'),
    path('reject_leave/', views.reject_leave, name='reject_leave'),
    path('lapsed_leave/', views.lapsed_leave, name='lapsed_leave'),

    # MANAGER
    path('manager/requests/', views.manager_leave_requests, name='manager_leave_requests'),
    path('manager/approve/<int:id>/', views.approve_leave_request, name='approve_leave_request'),
    path('manager/reject/<int:id>/', views.reject_leave_request, name='reject_leave_request'),


    path("my-leaves/", views.my_leave_requests, name="my_leave_requests"),
    path("cancel-leave/<int:id>/", views.cancel_leave, name="cancel_leave"),
]
