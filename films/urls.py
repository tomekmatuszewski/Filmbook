from django.urls import path

from films.views import FilmCreateView, FilmListView, FilmDetailView, film_likes

urlpatterns = [
    path("", FilmListView.as_view(), name="home"),
    path("add-film", FilmCreateView.as_view(), name="add-film"),
    path("film/<slug:slug>", FilmDetailView.as_view(), name="film-detail"),
    path("film-like/<slug:slug>", film_likes, name="film-like"),
]
