from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from films.filters import FilmFilter
from films.forms import FilmForm
from films.models import Film


class FilmListView(ListView):

    model = Film
    template_name = "films/home.html"
    context_object_name = "films"
    extra_context = {"title": "Home"}
    ordering = ["-publication_date"]
    paginate_by = 5

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
