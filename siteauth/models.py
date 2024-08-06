from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance: "User", filename):
    return "users/avatars/user_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_avatar = models.ImageField(blank=True, upload_to=user_directory_path)
    bio = models.TextField(max_length=500)