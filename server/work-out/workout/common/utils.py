from django.template.context_processors import csrf
from sport.models import Sport


def get_default_context(request, **kwargs):
    c = csrf(request)
    c.update(kwargs)
    c.update({"sports": Sport.objects.all()})
    return c
