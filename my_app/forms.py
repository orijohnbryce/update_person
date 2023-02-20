from django import forms
from django.forms import ModelForm

from .models import Car


class Search(forms.Form):

    file = forms.FileField(required=False)
    name = forms.CharField(max_length=20, required=False)


class CarForm(ModelForm):

    email = forms.EmailField(required=False)
    car_type = forms.CharField(max_length=20,
                               validators=[])

    class Meta:
        model = Car
        exclude = ["renters"]
        fields = "__all__"


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)



