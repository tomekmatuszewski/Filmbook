from django.urls import path


from films.views import FilmCreateView, FilmListView, FilmDetailView, film_likes, FilmUserListView, add_friend, FilmUpdateView, FilmDeleteView


urlpatterns = [
    path("", FilmListView.as_view(), name="home"),
    path("add-film", FilmCreateView.as_view(), name="add-film"),
    path("film/<slug:slug>", FilmDetailView.as_view(), name="film-detail"),
    path("film-like/<slug:slug>", film_likes, name="film-like"),

    path("film-user/<int:pk>", FilmUserListView.as_view(), name="film-user"),
    path("friends/<int:pk>", add_friend, name="friends-action"),

    path("film/update/<slug:slug>", FilmUpdateView.as_view(), name="film-update"),
    path("film/delete/<slug:slug>", FilmDeleteView.as_view(), name="film-delete"),

]
