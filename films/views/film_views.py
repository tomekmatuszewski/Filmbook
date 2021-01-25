from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from hitcount.views import HitCountDetailView

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from films.filters import FilmFilter

from films.forms import FilmForm, CommentForm
from films.models import Film, Comment
from django.contrib.auth.models import User


class FilmListView(ListView):

    model = Film
    template_name = "films/home.html"
    context_object_name = "films"
    extra_context = {"title": "Home"}
    ordering = ["-publication_date"]
    paginate_by = 10

    def paginate_filter_queryset(self):
        context = FilmFilter(self.request.GET, queryset=self.get_queryset()).qs
        paginate_by = self.get_paginate_by(context)
        page = self.request.GET.get("page", 1)

        paginator = Paginator(context, paginate_by)

        try:
            paginated_filter = paginator.page(page)
        except PageNotAnInteger:
            paginated_filter = paginator.page(1)
        except EmptyPage:
            paginated_filter = paginator.page(paginator.num_pages)
        return paginated_filter

    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = FilmFilter(self.request.GET, queryset=self.get_queryset())
        context["paginated_filter"] = self.paginate_filter_queryset()
        return context


class FilmCreateView(LoginRequiredMixin, CreateView):

    model = Film
    form_class = FilmForm
    template_name = "films/film_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FilmDetailView(UserPassesTestMixin, HitCountDetailView):

    model = Film
    template_name = "films/film_detail.html"
    count_hit = True

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_authenticated:
            admin = self.request.user.is_superuser
            author = obj.author == self.request.user
            friend = self.request.user.profile.friends.filter(id=obj.author.id)
            return not obj.isPrivate or admin or author or friend
        else:
            return not obj.isPrivate

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        # likes
        likes_connected = get_object_or_404(Film, slug=self.kwargs["slug"])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data["number_of_likes"] = likes_connected.total_likes
        data["post_is_liked"] = liked

        # comments
        comments_connected = Comment.objects.filter(film=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              title=request.POST.get('title'),
                              author=self.request.user,
                              film=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


def film_likes(request, slug):
    film = get_object_or_404(Film, id=request.POST.get("film_id"))
    if film.likes.filter(id=request.user.id).exists():
        film.likes.remove(request.user)
    else:
        film.likes.add(request.user)
    return HttpResponseRedirect(reverse("film-detail", args=[slug]))


class FilmUserListView(LoginRequiredMixin, ListView):

    model = Film
    template_name = "films/film_user.html"
    context_object_name = "films"
    ordering = ["-publication_date"]
    paginate_by = 10

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Film.objects.filter(author=User.objects.get(pk=user_id))

    def paginate_filter_queryset(self):
        context = FilmFilter(self.request.GET, queryset=self.get_queryset()).qs
        paginate_by = self.get_paginate_by(context)
        page = self.request.GET.get("page", 1)

        paginator = Paginator(context, paginate_by)

        try:
            paginated_filter = paginator.page(page)
        except PageNotAnInteger:
            paginated_filter = paginator.page(1)
        except EmptyPage:
            paginated_filter = paginator.page(paginator.num_pages)
        return paginated_filter

    def get_paginate_by(self, queryset):
        if self.request.GET.get("paginate_by") == "":
            return self.paginate_by
        return self.request.GET.get("paginate_by", self.paginate_by)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = FilmFilter(self.request.GET, queryset=self.get_queryset())
        context["paginated_filter"] = self.paginate_filter_queryset()
        return context


def add_friend(request, pk):

    user = User.objects.filter(pk=request.user.pk)

    if pk in list(user.values_list('profile__friends__id', flat=True)):
        request.user.profile.friends.remove(User.objects.get(pk=pk))
    else:
        request.user.profile.friends.add(User.objects.get(pk=pk))
    return HttpResponseRedirect(reverse("film-user", args=[pk]))


class FilmUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'films/film_form.html'
    model = Film
    form_class = FilmForm
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser


class FilmDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Film
    template_name = "films/film_delete.html"
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser

