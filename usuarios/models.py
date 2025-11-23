from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re


# ============================
# VALIDADORES DE RUT
# ============================

def validar_formato_rut(value):
    patron = r"^\d{7,8}-[\dkK]$"
    if not re.match(patron, value):
        raise ValidationError("El RUT debe tener el formato 12345678-9")


def validar_dv_rut(value):
    try:
        rut, dv = value.split("-")
    except ValueError:
        raise ValidationError("Formato RUT inválido")

    rut = rut[::-1]
    suma = 0
    multiplicador = 2

    for c in rut:
        suma += int(c) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    dv_calc = 11 - (suma % 11)

    if dv_calc == 11:
        dv_calc = "0"
    elif dv_calc == 10:
        dv_calc = "K"
    else:
        dv_calc = str(dv_calc)

    if dv.upper() != dv_calc:
        raise ValidationError("El dígito verificador es incorrecto")


# ============================
# MODELO DE USUARIO 
# ============================

class Usuarios(AbstractUser):
    rut = models.CharField(
        max_length=10,
        unique=False,
        validators=[validar_formato_rut, validar_dv_rut],
        help_text="Ingrese un RUT sin puntos. Ej: 12345678-9",
        blank=True,  # Permitir que el campo sea opcional ------TEMPORALMENTE-----------
    )

    telefono = models.CharField(max_length=13, blank=True, null=True)

    tipo_usuario = models.CharField(
        max_length=50,
        choices=[
            ('admin', 'Administrador'),
            ('cliente', 'Cliente'),
            ('trabajador', 'Trabajador'),
        ],
        default='cliente'
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
