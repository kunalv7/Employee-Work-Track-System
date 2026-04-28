"""
URL configuration for Employee_attendance_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')), # authenticate app urls
    path('leave_application/', include('leave_application.urls')), # leave_application app urls
    path('swipe_application/', include('swipe_application.urls')), # swipe_application app urls
    path('attendance_application/', include('attendance_application.urls')), # attendance_application app urls
    path('expense_application/', include('expense_application.urls')), # expense_application app urls
    path('my_attendance_application/', include('my_attendance_application.urls')), # my_attendance_application app urls
    path('self_service_application/', include('self_service_application.urls')), # self_service_application app urls
    path('quick_info_application/', include('quick_info_application.urls')), # quick_info_application app urls
    path('manager/', include('manager.urls')), # manager app urls
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)