from django.core.exceptions import ValidationError
from django.forms import (DecimalField, FileField, ModelForm)
from django.utils.text import slugify

from films.models import Film


class FilmForm(ModelForm):
    class Meta:
        model = Film
        exclude = ['publication_date', 'views_number', 'likes', 'slug', 'author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field, FileField):
                pass
            else:
                visible.field.widget.attrs["class"] = "form-control"

    def clean_title(self):
        title = self.cleaned_data['title']
        slug = slugify(title)
        # checking if title is in db, but not when we update current film
        if Film.objects.filter(slug=slug).exists() and not Film.objects.filter(id=self.instance.id).exists():
            raise ValidationError("The title already exists.Use unique film title")
        self.instance.slug = slug
        return title



