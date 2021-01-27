from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def ids_friends(user_id, film_author_id):
    user = User.objects.filter(pk=user_id)

    if film_author_id in list(user.values_list("profile__friends__id", flat=True)):

        return True
