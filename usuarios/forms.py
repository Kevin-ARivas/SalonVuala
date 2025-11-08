from django import forms
from .models import Usuarios
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "w-full bg-transparent border border-neutral-700 rounded p-3 focus:outline-none focus:border-[var(--accent)]"
        })
    )

    password2 = forms.CharField(
        label="Confirmar Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "w-full bg-transparent border border-neutral-700 rounded p-3 focus:outline-none focus:border-[var(--accent)]"
        })
    )

    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'telefono']
        widgets = {
            'username': forms.TextInput(attrs={"class": "w-full bg-transparent border border-neutral-700 rounded p-3 focus:outline-none focus:border-[var(--accent)]"}),
            'email': forms.EmailInput(attrs={"class": "w-full bg-transparent border border-neutral-700 rounded p-3 focus:outline-none focus:border-[var(--accent)]"}),
            'telefono': forms.TextInput(attrs={"class": "w-full bg-transparent border border-neutral-700 rounded p-3 focus:outline-none focus:border-[var(--accent)]"}),
        }

class UsuarioFormAdmin(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'telefono', 'password1', 'password2', 'tipo_usuario', 'tipo_usuario']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'telefono': forms.TextInput(),
        }