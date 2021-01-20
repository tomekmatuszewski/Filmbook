from django.urls import path

from films.views import FilmListView

urlpatterns = [
    path("", FilmListView.as_view(), name="home"),
]