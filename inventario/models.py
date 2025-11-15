from django.db import models

class Producto(models.Model):
    TIPO_CHOICES = [
        ("venta", "Venta al Cliente"),
        ("insumo", "Consumo Interno"),
    ]

    CATEGORIA_CHOICES = [
        ("shampoo", "Shampoo"),
        ("acondicionador", "Acondicionador"),
        ("mascarilla", "Mascarilla / Máscara"),
        ("aceite", "Aceite / Aceite"),
        ("otros", "Otros"),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="venta")

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default="otros"
    )

    precio = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)

    codigo_barra = models.CharField(max_length=50, unique=True)

    unidad = models.CharField(max_length=20, default="und")
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)

    def necesita_reposicion(self):
        return self.stock <= self.stock_minimo

    def __str__(self):
        return f"{self.nombre} (${self.precio})"
