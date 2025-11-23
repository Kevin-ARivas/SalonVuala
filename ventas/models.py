from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Venta(models.Model):
    total = models.IntegerField()
    metodo_pago = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    estilista = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Venta {self.id} - ${self.total}"




class Gasto(models.Model):
    descripcion = models.CharField(max_length=200)
    monto = models.IntegerField()
    categoria = models.CharField(max_length=100, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gasto {self.id} - ${self.monto} ({self.descripcion})"
