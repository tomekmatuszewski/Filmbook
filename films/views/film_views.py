from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from films.forms import FilmForm
from django.views.generic import ListView, CreateView
from films.models import Film


class FilmListView(ListView):

    model = Film
    template_name = "films/home.html"
    context_object_name = "films"
    extra_context = {"title": "Home"}
    ordering = ["-publication_date"]
    paginate_by = 5


class FilmCreateView(LoginRequiredMixin, CreateView):

    model = Film
    form_class = FilmForm
    template_name = 'films/film_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)