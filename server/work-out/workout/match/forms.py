from django import forms
from sport.models import Sport, Location

from .models import RequestMatch, Evaluation


class RequestMatchForm(forms.ModelForm):

    class Meta:
        model = RequestMatch
        fields = ('start_time', 'start_date', "end_time", "end_date", "with_similar_level",
                  'with_same_sex', 'show_personal_info', 'show_match_records', 'note', 'skillful')

    def __init__(self, *args, **kwargs):
        self.sports_list = [(o.id, o.name) for o in Sport.objects.all()]
        self.location_list = [(o.id, o.name) for o in Location.objects.all()]

        super(RequestMatchForm, self).__init__(*args, **kwargs)
        self.fields['sports'] = forms.ChoiceField(
            choices=self.sports_list
        )
        self.fields['location'] = forms.ChoiceField(
            choices=self.location_list
        )


class EvaluationForm(forms.ModelForm):

    class Meta:
        model = Evaluation
        fields = ('manner', 'skill', "comments")
