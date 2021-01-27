from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from films.forms import CommentForm
from films.models import Comment


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "films/comment_form.html"
    model = Comment
    form_class = CommentForm
    context_object_name = "comment"

    def get_success_url(self):
        return reverse_lazy("film-detail", kwargs={"slug": self.kwargs["slug"]})

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "films/comment_delete.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy("film-detail", kwargs={"slug": self.kwargs["slug"]})
