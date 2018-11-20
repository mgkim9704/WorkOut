from django.contrib import admin
from .models import RequestMatch, Match, Evaluation
# Register your models here.


@admin.register(RequestMatch)
class RequestMatchAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "sport", "location", "status", 'start_time', 'start_date', "end_time", "end_date"]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ["id", "player1", "player2", "location", "status", 'start_time', 'start_date']


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ["id", "writer", 'target', 'manner', 'skill', 'comments']

