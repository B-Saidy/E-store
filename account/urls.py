from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'account/login.html'), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(next_page = 'index'), name = 'logout'),
    path('profile/',views.profile, name='profile'),
    path('reset/',auth_views.PasswordResetView.as_view(template_name = 'account/password_reset.html'), name = 'password_reset'),
    path('reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'account/password_reset_done.html'), name = 'password_reset_done'),
    path('confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'account/password_reset_confirm.html'), name = 'password_reset_confirm'), # The pattern name: 'password_reset_confirm' is required
    path('confirm/complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'account/password_reset_complete.html')),

]
