from django import forms

from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['pid', 'name', 'phone', 'email', 'gender', 'birthday', 'introduction']

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['gender'].required = False
        self.fields['birthday'].required = False
        self.fields['introduction'].required = False

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ('name', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['pid', 'name', 'phone', 'email', 'gender', 'birthday', 'introduction', 'avatar']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'avatar': forms.FileInput(),
        }