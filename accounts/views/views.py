from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from accounts.forms import SignUpForm
from accounts.forms.forms import ProfileUpdateForm, UserUpdateForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup_form.html"


class MyLoginView(LoginView):
    template_name = 'accounts/form_login.html'


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/form_password_change.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your password has been changed.")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = User
    template_name = "accounts/user_profile.html"
    form_class = UserUpdateForm

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() and profile_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("home")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {"user_form": user_form, "profile_form": profile_form}
        return render(request, self.template_name, self.get_context_data(**context))

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False
