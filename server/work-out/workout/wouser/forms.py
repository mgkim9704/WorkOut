from django import forms


class SignupForm(forms.Form):
    uid = forms.CharField(max_length=10)
    pwd = forms.CharField(max_length=30)
    repwd = forms.CharField(max_length=30)
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    sex = forms.ChoiceField(choices=[("0", "woman"), ("1", "man")])
