from django.urls import path

from films.views import FilmCreateView, FilmListView, FilmDetailView, film_likes, FilmUserListView, \
    add_friend, FilmUpdateView, FilmDeleteView, CommentDeleteView, CommentUpdateView

from films.views.category_views import CategoryCreateView, CategoryListView, CategoryDeleteView, CategoryUpdateView


urlpatterns = [
    path("", FilmListView.as_view(), name="home"),
    path("add-film", FilmCreateView.as_view(), name="add-film"),
    path("film/<slug:slug>", FilmDetailView.as_view(), name="film-detail"),
    path("film-like/<slug:slug>", film_likes, name="film-like"),
    path("film-user/<int:pk>", FilmUserListView.as_view(), name="film-user"),
    path("friends/<int:pk>", add_friend, name="friends-action"),
    path("film/update/<slug:slug>", FilmUpdateView.as_view(), name="film-update"),
    path("film/delete/<slug:slug>", FilmDeleteView.as_view(), name="film-delete"),
    path('add-category', CategoryCreateView.as_view(), name='add-category'),
    path('category-list', CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),

    path("film/<slug:slug>/comment-update/<int:pk>", CommentUpdateView.as_view(), name="comment-update"),
    path("film/<slug:slug>/comment-delete/<int:pk>", CommentDeleteView.as_view(), name="comment-delete"),

]

