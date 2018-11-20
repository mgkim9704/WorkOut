from datetime import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from sport import models as sprorts_model


class RequestMatch(models.Model):
    FINDING = 0
    FOUND = 1
    PAUSE = 2
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    sport = models.ForeignKey(sprorts_model.Sport, on_delete=models.CASCADE, null=False)
    location = models.ForeignKey(sprorts_model.Location, on_delete=models.CASCADE, null=False)
    start_time = models.TimeField(default=timezone.now)
    start_date = models.DateField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    note = models.TextField(max_length=200, null=True, default="", blank=True)
    status = models.IntegerField(default=FINDING,
                                 choices=[(FINDING, "finding"), (FOUND, "found"), (PAUSE, "pause")])

    with_similar_level = models.BooleanField(default=False)
    with_same_sex = models.BooleanField(default=False)
    show_personal_info = models.BooleanField(default=False)
    show_match_records = models.BooleanField(default=False)
    skillful = models.IntegerField(default=0)

    match = models.ForeignKey('match.Match', default=None, null=True, blank=True, on_delete=models.SET_NULL)

    def from_to(self):
        return datetime.combine(self.start_date, self.start_time), datetime.combine(self.end_date, self.end_time)


class Match(models.Model):
    OPEN = 0
    MATCHED = 1
    PLAYING = 2
    FINISH = 3

    id = models.AutoField(primary_key=True)
    sport = models.ForeignKey(sprorts_model.Sport, on_delete=models.CASCADE, null=False)
    location = models.ForeignKey(sprorts_model.Location, on_delete=models.CASCADE, null=False)

    player1 = models.ForeignKey(User, related_name="player1", on_delete=models.SET_NULL, null=True, blank=True)
    player2 = models.ForeignKey(User, related_name="player2", on_delete=models.SET_NULL, null=True, blank=True)
    winner = models.ForeignKey(User, related_name="winner", on_delete=models.SET_NULL, null=True, blank=True)
    loser = models.ForeignKey(User, related_name="loser", on_delete=models.SET_NULL, null=True, blank=True)

    p1_approval = models.NullBooleanField(default=None)
    p2_approval = models.NullBooleanField(default=None)

    start_time = models.TimeField(default=timezone.now)
    start_date = models.DateField(default=timezone.now)
    status = models.IntegerField(default=0,
                                 choices=[(OPEN, "open"), (MATCHED, "matched"),
                                          (PLAYING, "playing"), (FINISH, "finish")])
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        if self.status == Match.FINISH:
            try:
                reqmats = RequestMatch.objects.filter(match=self)
                for reqmat in reqmats:
                    reqmat.status = RequestMatch.FINDING
                    reqmat.match = None
                    reqmat.save()
            except BaseException as e:
                print(e)
        return super(Match, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        try:
            reqmats = RequestMatch.objects.filter(match=self)
            for reqmat in reqmats:
                reqmat.status = RequestMatch.FINDING
                reqmat.match = None
                reqmat.save()
        except BaseException as e:
            print(e)
        return super(Match, self).delete(using, keep_parents)


class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    sport = models.ForeignKey(sprorts_model.Sport, on_delete=models.CASCADE, default=None, null=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    target = models.ForeignKey(User, related_name='evaluated_user', on_delete=models.CASCADE, default=None, null=True)
    manner = models.IntegerField()
    skill = models.IntegerField()
    comments = models.TextField(max_length=128)

