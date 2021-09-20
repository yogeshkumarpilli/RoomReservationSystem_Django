"""MeetingReserve URL Configuration

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
from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from system.views import *
from system.models import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('', HomePage.as_view(), name='homepage'),
    path('room/<int:pk>/', RoomView.as_view(), name='room-detail'),
    path('add-room/', AddRoom.as_view(), name='add-room'),
    path('modify-room/<int:pk>/', ModifyRoom.as_view(), name='modify-room'),
    path('delete-room/<int:pk>', DeleteRoom.as_view(), name='delete-room'),
    path('reservation/', MakeReservation.as_view(), name='make-reservation'),
    path('modify-reservation/<int:pk>/', UpdateReservation.as_view(), name='update-reservation'),
    path('delete-reservation/<int:pk>/', DeleteReservation.as_view(), name='delete-reservation'),
]