from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views.views import (MyLoginView, MyPasswordChangeView, SignUpView,
                                  UserUpdateView)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name='logout'),
    path('password-change/', MyPasswordChangeView.as_view(), name='password_change'),
    path('account/<int:pk>/profile-update/', UserUpdateView.as_view(), name='user_update')
]
