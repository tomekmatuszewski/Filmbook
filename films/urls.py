from django.urls import path

from films.views import (CommentDeleteView, CommentUpdateView, FilmCreateView,
                         FilmDeleteView, FilmDetailView, FilmListFriendsView,
                         FilmListView, FilmUpdateView, FilmUserListView,
                         film_likes, film_rate)
from films.views.category_views import (CategoryCreateView, CategoryDeleteView,
                                        CategoryListView, CategoryUpdateView)

urlpatterns = [
    path("", FilmListView.as_view(), name="home"),
    path("friends-films", FilmListFriendsView.as_view(), name="friends-films"),
    path("add-film", FilmCreateView.as_view(), name="add-film"),
    path("film/<slug:slug>", FilmDetailView.as_view(), name="film-detail"),
    path("film-like/<slug:slug>", film_likes, name="film-like"),
    path("film-user/<int:pk>", FilmUserListView.as_view(), name="film-user"),
    path("film/update/<slug:slug>", FilmUpdateView.as_view(), name="film-update"),
    path("film/delete/<slug:slug>", FilmDeleteView.as_view(), name="film-delete"),
    path("add-category", CategoryCreateView.as_view(), name="add-category"),
    path("category-list", CategoryListView.as_view(), name="categories"),
    path(
        "category/<int:pk>/update", CategoryUpdateView.as_view(), name="category-update"
    ),
    path(
        "category/<int:pk>/delete", CategoryDeleteView.as_view(), name="category-delete"
    ),
    path(
        "film/<slug:slug>/comment-update/<int:pk>",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "film/<slug:slug>/comment-delete/<int:pk>",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path("film-rate/<slug:slug>", film_rate, name="film-rate"),
]
