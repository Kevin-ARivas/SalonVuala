from django.db import models

# Create your models here.
class Sucursales(models.Model):
    nombre = models.CharField(max_length=30) 
    direccion = models.CharField(max_length=50)
    telefono = models.PositiveIntegerField()
    imagen = models.ImageField()

    def __str__(self):
        return f"Sucursal {self.nombre}."