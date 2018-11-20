from django.views import View
from django.http import *
from django.shortcuts import render
from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from elo import Rating, rate_1vs1

from .forms import RequestMatchForm, EvaluationForm, Evaluation
from .models import Match, RequestMatch
from common.utils import get_default_context
from sport.models import Sport, Ability
from wouser.utils import push_message
# Create your views here.


def get_me_and_you(request, match):
    if match.player1 == request.user:
        user2 = match.player2
    else:
        user2 = match.player1

    return request.user, user2


class RequestMatchView(LoginRequiredMixin, View):
    def get(self, request):
        form = RequestMatchForm(request.GET)
        c = get_default_context(request, form=form)
        return render(request, "request_form.html", c)

    def post(self, request):
        form = RequestMatchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            instance = form.save(commit=False)
            instance.user = request.user
            instance.location_id = cd["location"]
            instance.sport_id = cd["sports"]
            instance.save()

            return HttpResponseRedirect(reverse('my_matches'))
        c = get_default_context(request, form=form)

        return render(request, "request_form.html", c)


class MyMatchView(LoginRequiredMixin, View):
    def get(self, request):
        form = RequestMatchForm(request.GET)
        request_matches = RequestMatch.objects.filter(user=request.user)

        matches = Match.objects.filter((Q(player1=request.user) | Q(player2=request.user)))
        current_matches = matches.exclude(status=Match.FINISH)
        previous_matches = matches.filter(status=Match.FINISH)
        c = get_default_context(request, form=form,
                                request_matches=request_matches,
                                current_matches=current_matches,
                                previous_matches=previous_matches)
        return render(request, "myMatches.html", c)


class RequestListView(LoginRequiredMixin, View):
    def get(self, request):
        match_requests = RequestMatch.objects.all().exclude(user=request.user).filter(status=RequestMatch.FINDING)
        if "sports_filter" in request.GET:
            try:
                sport = Sport.objects.get(id=int(request.GET["sports_filter"]))
            except Exception:
                return render(request, "request_list.html", get_default_context(request))
            match_requests = match_requests.filter(sport=sport)

        c = get_default_context(request, match_requests=match_requests)
        return render(request, "request_list.html", c)


class MatchDetailView(LoginRequiredMixin, View):
    def get(self, request, match_number):
        try:
            match = Match.objects.get(id=match_number)
        except BaseException:
            return HttpResponseNotFound()
        if match.status == Match.OPEN:
            return HttpResponseRedirect(reverse('new_match', kwargs={"match_number": match_number}))

        if match.status == Match.FINISH and len(Evaluation.objects.filter(match=match, writer=request.user)) == 0:
            return HttpResponseRedirect(reverse('evaluation', kwargs={"match_number": match_number}))



        c = get_default_context(request, match=match)
        return render(request, "match_detail.html", c)


class MatchResultView(LoginRequiredMixin, View):
    def get(self, request, match_number):
        try:
            match = Match.objects.get(id=match_number)
        except BaseException:
            return HttpResponseNotFound()
        c = get_default_context(request, match=match)
        return render(request, "match_result.html", c)

    def post(self, request, match_number):
        try:
            match = Match.objects.get(id=match_number)
        except BaseException:
            return HttpResponseNotFound()

        if match.status != Match.PLAYING:
            return HttpResponseRedirect(reverse('match_detail', kwargs={"match_number": match_number}))

        user1, user2 = get_me_and_you(request, match)

        if request.POST["result"] == "Win":
            match.winner = user1
            match.loser = user2
        else:
            match.winner = user2
            match.loser = user1

        self.win(match.sport, match.winner, match.loser)

        match.status = Match.FINISH
        match.save()

        me, you = get_me_and_you(request, match)
        push_message(you, title="match is end '{}' win!".format(match.winner),
                     message="'{}' decided the result. please evaluate your partner '{}'".format(me, me))

        return HttpResponseRedirect(reverse('match_detail', kwargs={"match_number": match_number}))

    def win(self, sport, winner, loser, drawn=False):
        w_ability, l_ability = Ability.objects.get(user=winner, sport=sport), Ability.objects.get(user=loser, sport=sport)
        w_rating, l_rating = rate_1vs1(Rating(w_ability.rating), Rating(l_ability.rating), drawn)
        w_ability.rating = int(w_rating)
        l_ability.rating = int(l_rating)
        w_ability.save()
        l_ability.save()


class NetMatchView(LoginRequiredMixin, View):
    def get(self, request, match_number):
        try:
            match = Match.objects.get(id=match_number)
        except BaseException:
            return HttpResponseNotFound()

        user1, user2 = get_me_and_you(request, match)
        note = ""
        until = datetime.combine(match.start_date, match.start_time) - timedelta(hours=2)
        try:
            reqeust_match = RequestMatch.objects.get(user=user2, match=match)
            note = reqeust_match.note
        except BaseException:
            pass

        c = get_default_context(request, match=match, note=note, until=until)

        return render(request, "new_match.html", c)

    def post(self, request, match_number):
        try:
            match = Match.objects.get(id=match_number)
        except BaseException:
            return HttpResponseNotFound()

        if match.status != Match.OPEN:
            return HttpResponseRedirect(reverse('my_matches'))

        is_join = request.POST["result"] == "Join"

        if not is_join:
            self.rejected(request, match)
        else:
            self.joined(request, match)
        return HttpResponseRedirect(reverse('my_matches'))

    def rejected(self, request, match):
        for req_mat in RequestMatch.objects.filter(match=match):
            req_mat.status = RequestMatch.FINDING
            req_mat.match = None
            req_mat.save()

        me, you = get_me_and_you(request, match)
        push_message(you, title="match is rejected", message="{} vs {} match is canceled".format(me, you))
        match.delete()

    def joined(self, request, match):
        if match.player1 == request.user:
            match.p1_approval = True
        else:
            match.p2_approval = True

        if match.p1_approval and match.p2_approval:
            match.status = Match.MATCHED

        me, you = get_me_and_you(request, match)
        push_message(you, title="match is success!",
                     message="{} vs {} match in {} {}".format(me, you, match.start_date, match.start_time))
        match.save()


class ManualMatchView(LoginRequiredMixin, View):
    def get(self, request, request_number):
        try:
            reqmat = RequestMatch.objects.get(id=request_number)
        except BaseException:
            return HttpResponseNotFound()

        until = datetime.combine(reqmat.start_date, reqmat.start_time) - timedelta(hours=2)
        c = get_default_context(request, match=reqmat, until=until)

        return render(request, "request_new_match.html", c)

    def post(self, request, request_number):
        try:
            reqmat = RequestMatch.objects.get(id=request_number)
        except BaseException:
            return HttpResponseNotFound()

        if reqmat.status != RequestMatch.FINDING:
            return HttpResponseRedirect(reverse('request_list'))

        is_join = request.POST["result"] == "Join"

        if not is_join:
            return HttpResponseRedirect(reverse('request_list'))
        else:
            self.joined(request, reqmat)
        return HttpResponseRedirect(reverse('my_matches'))

    def joined(self, request, reqmat):
        match = Match(
            sport=reqmat.sport,
            location=reqmat.location,
            player1=request.user,
            player2=reqmat.user,
            p1_approval=True,
            start_time=reqmat.start_time,
            start_date=reqmat.start_date,
            status=Match.OPEN
        )
        match.save()

        push_message(match.player1, title="match is opened!",
                     message="{} vs {} match in {} {}".format(match.player1, match.player2, match.start_date, match.start_time))
        push_message(match.player2, title="match is opened!",
                     message="{} vs {} match in {} {}".format(match.player1, match.player2, match.start_date,
                                                              match.start_time))

        reqmat.match = match
        reqmat.status = RequestMatch.FOUND
        reqmat.save()


class EvaluationView(LoginRequiredMixin, View):
    def get(self, request, match_number):
        match = Match.objects.get(id=match_number)
        try:
            Evaluation.objects.get(match=match, writer=request.user)
            return HttpResponseRedirect('my_matches')
        except BaseException:
            pass
        user1, user2 = get_me_and_you(request, match)
        c = get_default_context(request, target=user2, match=match)
        return render(request, 'evaluation.html', c)

    def post(self, request, match_number):
        match = Match.objects.get(id=match_number)
        form = EvaluationForm(request.POST)
        print(request.POST)
        user1, user2 = get_me_and_you(request, match)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.match = match
            evaluation.writer = user1
            evaluation.target = user2
            evaluation.sport = match.sport
            evaluation.save()
            return HttpResponseRedirect(reverse('my_matches'))

        return HttpResponseRedirect(reverse('evaluation', kwargs={"match_number": match_number}))
