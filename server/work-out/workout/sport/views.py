from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from common.utils import get_default_context
from .models import Ability, Sport
from match.models import Evaluation
from match.models import Match, RequestMatch
from django.contrib.auth.models import User


class SportMain(LoginRequiredMixin, View):
    def get(self, request, sport_name):
        sport = Sport.objects.get(name=sport_name.replace('-', ' '))
        ability = Ability.objects.get(user=request.user, sport=sport)
        request_matches = RequestMatch.objects.exclude(user=request.user).filter(status=RequestMatch.FINDING).order_by('-id')[:4]
        matches = Match.objects.filter(status=Match.MATCHED, sport=sport).order_by('-id')[:4]
        c = get_default_context(
            request,
            sport_name=sport.name.title(),
            ability=ability,
            win_count=len(Match.objects.filter(winner=request.user, sport=sport)),
            lose_count=len(Match.objects.filter(loser=request.user, sport=sport)),
            bar_value=ability.rating / 3000 * 100,
            request_matches=request_matches,
            matches=matches
        )
        return render(request, 'sport_detail.html', c)


class PlayerDetailView(LoginRequiredMixin, View):
    def get(self, request, sport_name, user_id):
        target = User.objects.get(id=user_id)
        sport = Sport.objects.get(name=sport_name.replace('-', ' '))
        ability = Ability.objects.get(user=target, sport=sport)
        comments = Evaluation.objects.filter(target=target)
        lose_count = len(Match.objects.filter(loser=request.user, sport=sport))
        win_count = len(Match.objects.filter(winner=request.user, sport=sport))

        c = get_default_context(request, target=target, ability=ability, comments=comments,
                                lose_count=lose_count, win_count=win_count)
        return render(request, 'player_detail.html', c)
