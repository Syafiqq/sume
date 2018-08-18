from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120,
                               label="Username")
    password = forms.CharField(max_length=120,
                               label="Password")
