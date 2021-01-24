from django.contrib import admin

from films.models import Category, Comment, Film

# Register your models here.

admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Film)
