"""StockCheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
import account.views

urlpatterns = [
    # paths for general account authentication and management
    path('login/', account.views.log_in, name="login"),
    path('signup/', account.views.signup, name="signup"),
    path('logout/', account.views.log_out, name="logout"),
    path('management/', account.views.management, name="management"),
    path('management/password_change/', account.views.password_change, name="password_change"),

    # paths for password resetting
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="password_management/password_reset.html"),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_management/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_management/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_management/password_reset_complete.html"),
         name='password_reset_complete'),
]
