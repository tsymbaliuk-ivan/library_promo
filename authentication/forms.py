from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'password', 'role']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)