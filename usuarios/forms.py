# usuarios/forms.py
from django import forms
from .models import Usuario

class LoginForm(forms.Form):
    Username = forms.CharField(max_length=50, label="Nome de Usuário")
    Senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
