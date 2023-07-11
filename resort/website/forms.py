from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class LoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100,widget=forms.PasswordInput)


class RegistraionForm(UserCreationForm):
    class Meta:
        model = User
        fields=['first_name','last_name','username','password1','password2']


class CheckIn(forms.Form):
    Indate=forms.DateField()
    Outdate=forms.DateField()
    Adults=forms.IntegerField()
    Kids=forms.IntegerField()