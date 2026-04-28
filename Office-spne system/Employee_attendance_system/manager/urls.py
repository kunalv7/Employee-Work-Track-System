from django.urls import path
from . import views

urlpatterns = [
    # =====================================
    # 🔐 MANAGER LOGIN / LOGOUT
    # =====================================
    path('login/', views.manager_login, name='manager_login'),
    path('manager_logout/', views.manager_logout_view, name='manager_logout'),

    # =====================================
    # 👨‍💼 DASHBOARD
    # =====================================
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),

    # =====================================
    # 📥 SWIPE REQUESTS
    # =====================================
    path('swipe_request/', views.swipe_request, name='swipe_request'),
    path('approve/<int:id>/', views.approve_request, name='approve_request'),
    path('reject/<int:id>/', views.reject_request, name='reject_request'),

    # =====================================
    # 📝 LEAVE REQUESTS
    # =====================================
    path('manager/requests/', views.manager_leave_requests, name='manager_leave_requests'),
    path('manager/approve/<int:id>/', views.approve_leave_request, name='approve_leave_request'),
    path('manager/reject/<int:id>/', views.reject_leave_request, name='reject_leave_request'),

    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:user_id>/attendance/', views.view_employee_attendance, name='view_employee_attendance'),

    path("employee/<int:user_id>/swipes/", views.employee_swipe_details, name="employee_swipe_details"),
    path("employee/<int:user_id>/leaves/", views.employee_leave_details, name="employee_leave_details"),

    path("employee/<int:user_id>/analytics/", views.employee_analytics, name="employee_analytics"),
    path('employee/<int:id>/', views.employee_info, name='employee_info'),

]