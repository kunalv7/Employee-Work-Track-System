from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('home/', views.home, name='home'),
    path('user_logout/', views.logout_view, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path("id-card/", views.id_card, name="id_card"),
]