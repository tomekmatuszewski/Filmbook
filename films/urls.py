from django.urls import path

from films.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]