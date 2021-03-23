from .models import Progs
from django import forms


class Register(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required="")


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.py'}),required=None)


class Git_form(forms.Form):
    git_link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
