from django.urls import re_path
from django.conf.urls import url
from .views import *

urlpatterns = [
    re_path(r'^request[/]$', RequestMatchView.as_view(), name="request_match"),
    re_path(r'^my-matches[/]$', MyMatchView.as_view(), name="my_matches"),
    re_path(r'^request-list[/]$', RequestListView.as_view(), name="request_list"),
    re_path(r'^match-detail/(?P<match_number>[0-9]+)$', MatchDetailView.as_view(), name="match_detail"),
    re_path(r'^match-result/(?P<match_number>[0-9]+)$', MatchResultView.as_view(), name="match_result"),
    re_path(r'^new-match/(?P<match_number>[0-9]+)$', NetMatchView.as_view(), name="new_match"),
    re_path(r'^manual-match/(?P<request_number>[0-9]+)$', ManualMatchView.as_view(), name="manual_match"),
    re_path(r'^evaluation/(?P<match_number>[0-9]+)$', EvaluationView.as_view(), name="evaluation"),
]
