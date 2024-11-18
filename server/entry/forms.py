from django import forms

from .models import Entry

class EntryForm:
    class Meta:
        model = Entry
        fields = ['eid', 'tid', 'time', 'place', 'description']