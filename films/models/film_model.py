from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Film(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    isPublic = models.BooleanField()
    publication_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    video = models.FileField(upload_to='videos')
    views_number = models.IntegerField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='films')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='films')

    likes = models.ManyToManyField(User)
    tags = TaggableManager()

    def __str__(self) -> str:
        return f'{self.title}'

    @property
    def total_likes(self) -> int:
        return self.likes.count()

    def get_absolute_url(self) -> str:
        return reverse("film-detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')

    def __str__(self) -> str:
        return f'{self.title}'
