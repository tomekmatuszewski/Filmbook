from django.contrib import admin

from films.models import Category, Comment, Film, Rating

# Register your models here.

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Film)
admin.site.register(Rating)
