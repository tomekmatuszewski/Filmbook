from django.urls import path

from films.views import FilmListView, FilmCreateView

urlpatterns = [
    path("", FilmListView.as_view(), name="home"),
    path("add-film", FilmCreateView.as_view(), name="add-film"),
]