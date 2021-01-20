from django.shortcuts import render

from django.views.generic import ListView
from films.models import Film


class FilmListView(ListView):

    model = Film
    template_name = "films/home.html"
    context_object_name = "films"
    extra_context = {"title": "Home"}
    ordering = ["-publication_date"]
    paginate_by = 5