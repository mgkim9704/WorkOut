from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Sport(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='icon/', default=None, null=True)
    icon2 = models.ImageField(upload_to='icon2/', default=None, null=True)

    def save(self, *args, **kwargs):
        created = False
        if not self.id:
            created = True

        ret = super(Sport, self).save(*args, **kwargs)

        if created:
            for user in User.objects.all():
                Ability.objects.create(user=user, sport=self)

        return ret

    def __str__(self):
        return self.name

    def get_url_name(self):
        return str(self.name).replace(' ', '-')


class Ability(models.Model):
    id = models.AutoField(primary_key=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1000)

    def __str__(self):
        return self.rating


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    x_pos = models.FloatField(blank=True, null=True, default=0)
    y_pos = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_abilities(sender, instance, created, **kwargs):
    if created:
        for sport in Sport.objects.all():
            Ability.objects.create(user=instance, sport=sport)

