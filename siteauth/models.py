import os

from django.contrib.auth.models import User
from django.db import models

from News_Quest.settings import BASE_DIR


def user_directory_path(instance: "User", filename):
    return "users/avatars/user_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_avatar = models.ImageField(blank=True, upload_to=user_directory_path)
    bio = models.TextField(max_length=500)

    def save(self, *args, **kwargs):
        if not self.user_avatar:
            self.user_avatar = os.path.join(BASE_DIR, 'uploads/users/avatars/blank_avatar.png')
        super().save(*args, **kwargs)


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
