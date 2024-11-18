from django import forms

from .models import Picture, Picture_Album

class PictureForm(forms.ModelForm):
    model = Picture
    fields = ['pid', 'creator', 'create_time', 'file_name', 'image']
