from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField(default=0)
    codigo_barra = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.nombre} (${self.precio})"
