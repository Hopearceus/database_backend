from django import forms

from .models import Trip, Trip_Person


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['tid', 'name', 'time', 'creator', 'description']


class Trip_PersonForm(forms.ModelForm):
    class Meta:
        model = Trip_Person
        fields = ['tid', 'pid', 'notes']