from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_pics', default='default.png')
    friends = models.ManyToManyField(User, related_name='friends')
    about = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} profile"
