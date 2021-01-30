from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profile_pics", default="default.png")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    friends_requests = models.ManyToManyField(
        User, blank=True, related_name="friends_requests"
    )
    about = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} profile"
