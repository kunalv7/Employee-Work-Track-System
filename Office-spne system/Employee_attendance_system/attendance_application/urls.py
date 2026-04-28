from django.urls import path
from . import views

urlpatterns = [
    path('attendance_home/', views.attendance_home, name='attendance_home'),
    path('clock_in_attendance/', views.clock_in_attendance, name='clock_in_attendance'),
    path('clock_out_attendance/', views.clock_out_attendance, name='clock_out_attendance'),
    path('list_attendance/', views.list_attendance, name='list_attendance'),
]