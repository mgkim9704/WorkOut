from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=20, blank=True)
    sex = models.IntegerField(default=0, blank=True, choices=[(0, "man"), (1, "woman")])
    balance = models.IntegerField(default=1000, blank=True)
    additional = models.TextField(default=0, max_length=500, blank=True)
    fcm_registration_id = models.CharField(max_length=500, null=True, blank=True, default=None)

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()