import os
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workout.settings')

import django
from django.utils import timezone

django.setup()

from match.models import Match
from wouser.utils import push_message

matches = Match.objects.filter(status=Match.MATCHED)
playing = Match.objects.filter(status=Match.PLAYING)
now = timezone.now()
for match in matches:
    if timezone.make_aware(datetime.combine(match.start_date, match.start_time)) < now:
        match.status = Match.PLAYING
        push_message(match.player1, title="match is started! GG!",
                     message="{} vs {} match is started!".format(match.player1, match.player2))
        push_message(match.player2, title="match is started! GG!",
                     message="{} vs {} match is started!".format(match.player2, match.player1))
        match.save()

for match in playing:
    combine = timezone.make_aware(datetime.combine(match.start_date, match.start_time))
    if combine + timedelta(hours=2) <= now < combine + timedelta(hours=2, minutes=2):
        push_message(match.player1, title="Did you enjoy the game? ",
                     message="Please select game result!")
        push_message(match.player2, title="Did you enjoy the game?",
                     message="Please select game result!")

