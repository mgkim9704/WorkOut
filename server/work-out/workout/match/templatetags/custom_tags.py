from django import template
from sport.models import Ability
register = template.Library()


@register.simple_tag
def get_rating(user, sport):
    return str(Ability.objects.get(user=user, sport=sport).rating)


@register.filter
def get_rating_bar(rating):
    return int(rating) / 3000 * 100
