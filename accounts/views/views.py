from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from accounts.forms import SignUpForm
from accounts.forms.forms import ProfileUpdateForm, UserUpdateForm
from accounts.models import Profile


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup_form.html"


class MyLoginView(LoginView):
    template_name = "accounts/form_login.html"


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/form_password_change.html"
    success_url = reverse_lazy("home")

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


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = User
    template_name = "accounts/delete_account.html"

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False

    def get_success_url(self):
        messages.error(self.request, "Your account successfully deleted")
        return reverse_lazy("home")


class FriendsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    template_name = "accounts/friends.html"

    def test_func(self):
        return self.get_object() == self.request.user.profile


def add_friend(request, pk):
    user = User.objects.filter(pk=request.user.pk)
    if pk in list(user.values_list("profile__friends__id", flat=True)):
        request.user.profile.friends.remove(User.objects.get(pk=pk))
        User.objects.get(pk=pk).profile.friends.remove(request.user)
    else:
        User.objects.get(pk=pk).profile.friends_requests.add(request.user)
    return HttpResponseRedirect(reverse("film-user", args=[pk]))


def accept_friend(request, pk):
    user = request.user
    friend = User.objects.get(pk=pk)
    if request.POST.get("accept") == "accept":
        user.profile.friends.add(friend)
        friend.profile.friends.add(user)
        if friend.profile.friends_requests.filter(id=user.id).exists():
            friend.profile.friends_requests.remove(user)
    user.profile.friends_requests.remove(friend)
    return HttpResponseRedirect(reverse("friends-list", args=[user.pk]))
