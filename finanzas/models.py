from django.db import models


class Gasto(models.Model):
    descripcion = models.CharField(max_length=200)
    monto = models.IntegerField()
    categoria = models.CharField(max_length=100, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gasto {self.id} - ${self.monto} ({self.descripcion})"
    
class MovimientoCaja(models.Model):
    TIPO_CHOICES = (
        ("INGRESO", "Ingreso"),
        ("EGRESO", "Egreso"),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.IntegerField()
    descripcion = models.CharField(max_length=255)

    # Relación opcional con una venta
    venta = models.ForeignKey(
        "ventas.Venta",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.tipo} - ${self.monto}"