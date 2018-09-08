from django import forms


class Login(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class Register(forms.Form):
    username = forms.CharField()
    role = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    password_conf = forms.CharField()


class Forgot(forms.Form):
    email = forms.EmailField()


class Recover(forms.Form):
    token = forms.CharField()
    password = forms.CharField()
    password_conf = forms.CharField()
