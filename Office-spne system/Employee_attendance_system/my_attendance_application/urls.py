from django.urls import path
from . import views

urlpatterns = [
    path('my_attendance_home/', views.my_attendance_home, name='my_attendance_home')

    
]