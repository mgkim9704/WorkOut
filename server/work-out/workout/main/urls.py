
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path, re_path
from .views import test_html

urlpatterns = [
    re_path('test/(?P<html_name>[a-zA-Z0-9_.]+)', test_html),
]
