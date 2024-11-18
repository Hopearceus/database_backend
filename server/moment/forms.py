from django import forms

from .models import Moment, Moment_Person
from ..picture.models import Picture_Moment

class MomentForm(forms.ModelForm):
    class Meta:
        model = Moment
        fields = ['mid', 'creator', 'text', 'tid']
    
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.fields['tid'].required = False
        self.fields['text'].reqired = False

class Picture_MomentForm(forms.ModelForm):
    class Meta:
        model = Picture_Moment
        fields = ['pid', 'mid']