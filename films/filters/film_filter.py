import django_filters
from django.forms import CheckboxInput
from django_filters.widgets import RangeWidget
from django.db.models import BooleanField
from films.models import Film, Category

# based on django filters


class FilmFilter(django_filters.FilterSet):

    CHOICES = (("ascending", "Ascending"), ("descending", "Descending"))

    title = django_filters.CharFilter(
        label="Title", field_name="title", lookup_expr="icontains"
    )

    # tags = django_filters.CharFilter(
    #     label="Tags", field_name="tags", lookup_expr="icontains"
    # )

    category = django_filters.ModelChoiceFilter(
        label="Category", queryset=Category.objects.all(), field_name="category"
    )

    ordering_by_date = django_filters.ChoiceFilter(
        label="Ordering by Publication Date", choices=CHOICES, method="filter_by_order_date"
    )

    ordering_by_views = django_filters.ChoiceFilter(
        label="Ordering by Views Number", choices=CHOICES, method="filter_by_order_views"
    )

    rating = django_filters.RangeFilter(
        label="Rating Between",
        field_name="rating",
        widget=RangeWidget(attrs={"class": "textinput textInput form-control"}),
    )

    isPublic = django_filters.BooleanFilter(label="Is Public", field_name="isPublic",
                                            widget=CheckboxInput)

    class Meta:
        model = Film
        fields = ["title", "category", "rating", "isPublic"]


    @staticmethod
    def filter_by_order_date(queryset, name, value):
        expression = "publication_date" if value == "ascending" else "-publication_date"
        return queryset.order_by(expression)

    @staticmethod
    def filter_by_order_views(queryset, name, value):
        expression = "views_number" if value == "ascending" else "-views_number"
        return queryset.order_by(expression)


