from django import forms
from .models import Usuarios
from django.contrib.auth.forms import UserCreationForm
import re


class UsuarioForm(UserCreationForm):

    # --------------------------
    # CAMPOS PASSWORD
    # --------------------------
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

    # --------------------------
    # RUT
    # --------------------------
    rut = forms.CharField(
        label="RUT",
        max_length=12,
        widget=forms.TextInput(attrs={
            "placeholder": "12345678-9",
            "class": "w-full bg-transparent border border-neutral-700 rounded p-3 focus:outline-none focus:border-[var(--accent)]"
        })
    )

    # --------------------------
    # VALIDACIÓN RUT COMPLETA
    # --------------------------
    def clean_rut(self):
        rut = self.cleaned_data["rut"]

        # Validación formato: 12345678-9
        patron = r"^\d{7,8}-[\dkK]$"
        if not re.match(patron, rut):
            raise forms.ValidationError("El RUT debe tener el formato 12345678-9")

        # Validación DV — segura
        cuerpo, dv = rut.split("-")
        cuerpo = cuerpo[::-1]

        suma = 0
        mult = 2

        for c in cuerpo:
            suma += int(c) * mult
            mult = 2 if mult == 7 else mult + 1

        dv_calc = 11 - (suma % 11)
        if dv_calc == 11:
            dv_calc = "0"
        elif dv_calc == 10:
            dv_calc = "K"
        else:
            dv_calc = str(dv_calc)

        if dv.upper() != dv_calc:
            raise forms.ValidationError("El dígito verificador es incorrecto")

        return rut

    # --------------------------
    # META
    # --------------------------
    class Meta:
        model = Usuarios
        fields = ['rut', 'username', 'email', 'telefono']
        widgets = {
            'rut': forms.TextInput(attrs={"class": "w-full bg-transparent border border-neutral-700 rounded p-3"}),
            'username': forms.TextInput(attrs={"class": "w-full bg-transparent border border-neutral-700 rounded p-3"}),
            'email': forms.EmailInput(attrs={"class": "w-full bg-transparent border border-neutral-700 rounded p-3"}),
            'telefono': forms.TextInput(attrs={"class": "w-full bg-transparent border border-neutral-700 rounded p-3"}),
        }

    # --------------------------
    # ENCRIPTACIÓN SEGURA
    # --------------------------
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        usuario.is_verified = False   # 🔐 Usuario NO verificado aún
        if commit:
            usuario.save()
        return usuario



# =======================================================================
#                         FORMULARIO ADMIN
# =======================================================================

class UsuarioFormAdmin(UserCreationForm):

    rut = forms.CharField(
        label="RUT",
        max_length=12,
        widget=forms.TextInput(attrs={"placeholder": "12345678-9"})
    )

    class Meta:
        model = Usuarios
        fields = [
            'rut','username', 'email', 'telefono',
            'password1', 'password2', 'tipo_usuario'
        ]
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'tipo_usuario': forms.Select(),
        }

    # --------------------------
    # ENCRIPTACIÓN SEGURA ADMIN
    # --------------------------
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        if commit:
            usuario.save()
        return usuario
