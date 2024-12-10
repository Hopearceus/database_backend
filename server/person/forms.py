# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User

# from .models import Person

# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = ['pid', 'username', 'phone', 'email', 'gender', 'birthday', 'description']

#     def __init__(self, *args, **kwargs):
#         super.__init__(*args, **kwargs)
#         self.fields['phone'].required = False
#         self.fields['gender'].required = False
#         self.fields['birthday'].required = False
#         self.fields['description'].required = False

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = Person
#         fields = ('username', 'email', 'password')

# class CustomAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = Person

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = ['pid', 'username', 'phone', 'email', 'gender', 'birthday', 'description', 'avatar']
#         widgets = {
#             'birthday': forms.DateInput(attrs={'type': 'date'}),
#             'avatar': forms.FileInput(),
#         }