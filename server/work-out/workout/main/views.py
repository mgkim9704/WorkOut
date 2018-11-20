from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from common.utils import get_default_context

from match.models import RequestMatch, Match
# Create your views here.


class Main(View):
    def get(self, request):
        if not request.user.id:
            request_matches = RequestMatch.objects.filter(status=RequestMatch.FINDING).order_by('-id')[:4]
        else:
            request_matches = RequestMatch.objects.exclude(user=request.user).filter(status=RequestMatch.FINDING).order_by('-id')[:4]
        matches = Match.objects.filter(status=Match.MATCHED).order_by('-id')[:4]

        return render(request, 'main.html',
                      get_default_context(request, request_matches=request_matches, matches=matches))


def test_html(req, html_name):
    template = loader.get_template(html_name)
    return HttpResponse(template.render({"mylist": [
        {
            "first_name": "yun",
            "last_name": "ho",
            "age": 123,
            "flag": True,
        },
        {
            "first_name": "yun",
            "last_name": "3231",
            "age": 123,
            "flag": False,
        },
    ]}))
