from django import forms
from .models import Profile, User

from django.contrib.auth.forms import UserCreationForm


# forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email","password1","password2",)
