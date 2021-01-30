from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def ids_friends_requests(user_id, film_author_id):
    author = User.objects.filter(pk=film_author_id)
    return user_id in list(author.values_list("profile__friends_requests__id", flat=True))
