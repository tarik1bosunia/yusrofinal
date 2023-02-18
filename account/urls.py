from django.urls import path
from account import views

urlpatterns = [
    path('registration/', views.user_registration_view, name='user_registration'),
    path('profile/', views.user_profile_view, name='user_profile'),
    path('login/', views.user_login_view, name='user_login'),
    path('logout/', views.user_logout_view, name='user_logout'),
    path('changepassword/', views.user_change_password_view, name='user_change_password'),
    path('resetpassword/', views.user_reset_password_view, name='user_reset_password'),
    path('forgottenpassword/', views.user_forgotten_password_view, name='user_forgotten_password'),
]
