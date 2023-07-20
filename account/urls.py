from django.urls import path
from account import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_profile_view, name='user_profile'),
    path('registration/', views.user_registration_view, name='user_registration'),
    path('profile/', views.user_profile_view, name='user_profile'),
    path('settings_and_privacy/', views.user_settings_and_privacy_view, name='user_settings_and_privacy'),
    path('login/', views.user_login_view, name='user_login'),
    path('logout/', views.user_logout_view, name='user_logout'),
    path('activate/<uidb64>/<token>/', views.user_activate_view, name='user_activate'),
    path('changepassword/', views.user_change_password_view, name='user_change_password'),
    path('forgottenpassword/', views.user_forgotten_password_view, name='user_forgotten_password'),
    path('reset_password/confirm/<uidb64>/<token>/', views.user_reset_password_confirm_view, name='user_password_reset_confirm'),
    path('reset_password/', views.user_reset_password_view, name='user_reset_password'),

    # path('reset_password/', views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password/done/',  views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #
    # path('reset_password/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'),
    #      name='password_reset_sent'),
]
