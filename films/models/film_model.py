from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from hitcount.models import HitCount, HitCountMixin
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Film(models.Model, HitCountMixin):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    isPrivate = models.BooleanField()
    publication_date = models.DateTimeField(default=timezone.now)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    video = models.FileField(upload_to="videos", blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="films", null=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="films")

    likes = models.ManyToManyField(User, blank=True, related_name="film_likes")
    tags = TaggableManager()
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )
    gif = models.FileField(upload_to="gifs", blank=True)
    poster = models.ImageField(upload_to="posters", blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def total_likes(self) -> int:
        return self.likes.count()

    def get_absolute_url(self) -> str:
        return reverse("film-detail", kwargs={"slug": self.slug})

    @property
    def current_hit_count(self) -> int:
        return self.hit_count.hits

    @property
    def number_of_comments(self):
        return Comment.objects.filter(film=self).count()


class Comment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ["date_posted"]

    def __str__(self) -> str:
        return f"{self.title}"


class Rating(models.Model):
    rate = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rate")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="rate")

    def __str__(self) -> str:
        return f"{self.film} - {self.user} - {self.rate}"
