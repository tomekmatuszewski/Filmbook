import django_filters
from django.forms import CheckboxInput
from django_filters.widgets import RangeWidget

from films.models import Category, Film

# based on django filters


class FilmFilter(django_filters.FilterSet):

    CHOICES = (("ascending", "Ascending"), ("descending", "Descending"))

    title = django_filters.CharFilter(
        label="Title", field_name="title", lookup_expr="icontains"
    )

    tags = django_filters.CharFilter(
        label="Tag", field_name="tags", method="filter_by_tag"
    )

    category = django_filters.ModelChoiceFilter(
        label="Category", queryset=Category.objects.all(), field_name="category"
    )

    ordering_by_date = django_filters.ChoiceFilter(
        label="Ordering by Publication Date",
        choices=CHOICES,
        method="filter_by_order_date",
    )

    ordering_by_views = django_filters.ChoiceFilter(
        label="Ordering by Views Number",
        choices=CHOICES,
        method="filter_by_order_views",
    )

    rating = django_filters.RangeFilter(
        label="Rating Between",
        field_name="rating",
        widget=RangeWidget(attrs={"class": "textinput textInput form-control"}),
    )

    class Meta:
        model = Film
        fields = ["title", "category", "rating"]

    @staticmethod
    def filter_by_order_date(queryset, name, value):
        expression = "publication_date" if value == "ascending" else "-publication_date"
        return queryset.order_by(expression)

    @staticmethod
    def filter_by_order_views(queryset, name, value):
        expression = (
            "hit_count_generic" if value == "ascending" else "-hit_count_generic"
        )
        return queryset.order_by(expression)

    @staticmethod
    def filter_by_tag(queryset, name, value):
        return queryset.filter(tags__name__icontains=value)
