from django.urls import re_path
from django.conf.urls import url
from .views import *

urlpatterns = [
    re_path(r'^(?P<sport_name>[a-z-]+)$', SportMain.as_view(), name="sport_main"),
    re_path(r'^(?P<sport_name>[a-z-]+)/(?P<user_id>[0-9]+)$', PlayerDetailView.as_view(), name="player_detail"),
]
