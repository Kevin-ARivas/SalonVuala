from django.db import models

class Venta(models.Model):
    total = models.IntegerField()
    metodo_pago = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id} - ${self.total}"


class Gasto(models.Model):
    descripcion = models.CharField(max_length=200)
    monto = models.IntegerField()
    categoria = models.CharField(max_length=100, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gasto {self.id} - ${self.monto} ({self.descripcion})"
