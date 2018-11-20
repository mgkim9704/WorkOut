from django.contrib import admin
from .models import Sport
from .models import Sport, Ability, Location
# Register your models here.


@admin.register(Sport)
class SportsAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Ability)
class LevelAdmin(admin.ModelAdmin):
    list_display = ["id", "sport", "user", "rating"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

