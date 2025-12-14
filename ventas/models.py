from django.db import models
from django.contrib.auth import get_user_model
from inventario.models import Producto
from agenda.models import Servicio

User = get_user_model()


class Venta(models.Model):
    total = models.IntegerField()
    metodo_pago = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    estilista = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Venta {self.id} - ${self.total}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        related_name="detalles",
        on_delete=models.CASCADE
    )

    producto = models.ForeignKey(
        Producto,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    servicio = models.ForeignKey(
        Servicio,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    cantidad = models.PositiveIntegerField(default=1)
    precio = models.IntegerField()

    def __str__(self):
        return f"Detalle venta {self.venta.id}"
