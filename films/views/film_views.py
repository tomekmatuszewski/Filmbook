from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView

from films.forms import FilmForm
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
    template_name = "films/film_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FilmDetailView(DetailView):

    model = Film
    template_name = "films/film_detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        likes_connected = get_object_or_404(Film, slug=self.kwargs['slug'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.total_likes
        data['post_is_liked'] = liked
        return data


def film_likes(request, slug):
    film = get_object_or_404(Film, id=request.POST.get('film_id'))
    if film.likes.filter(id=request.user.id).exists():
        film.likes.remove(request.user)
    else:
        film.likes.add(request.user)
    return HttpResponseRedirect(reverse('film-detail', args=[slug]))
