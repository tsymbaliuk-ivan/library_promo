from django import forms
from .models import CustomUser
from django_recaptcha.fields import ReCaptchaField


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'password', 'role']

    captcha = ReCaptchaField()



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()