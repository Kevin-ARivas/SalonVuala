from django.db import models


class Gasto(models.Model):
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gasto #{self.id} - ${self.monto} ({self.descripcion})"


class MovimientoCaja(models.Model):
    TIPO_CHOICES = (
        ("INGRESO", "Ingreso"),
        ("EGRESO", "Egreso"),
    )

    ORIGEN_CHOICES = (
        ("VENTA", "Venta"),
        ("GASTO", "Gasto"),
        ("AJUSTE", "Ajuste Manual"),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    origen = models.CharField(
        max_length=10,
        choices=ORIGEN_CHOICES,
        default="VENTA"
    )

    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255)

    venta = models.ForeignKey(
        "ventas.Venta",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    gasto = models.ForeignKey(
        "finanzas.Gasto",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.tipo} - ${self.monto} ({self.origen})"
