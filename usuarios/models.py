from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuarios(AbstractUser):
    telefono = models.CharField(max_length=13, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=50, choices=[
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador'),
    ], default='cliente')

    def __str__(self):
        return self.username
