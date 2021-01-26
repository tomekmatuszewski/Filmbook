from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views.views import (MyLoginView, MyPasswordChangeView, SignUpView,
                                  UserUpdateView, UserDeleteView)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name="accounts/logout.html"), name='logout'),
    path('password-change/', MyPasswordChangeView.as_view(), name='password-change'),
    path('account/profile/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('account/profile/<int:pk>/delete', UserDeleteView.as_view(), name='user-delete')
]

