from django.db import models
from django.conf import settings  # ✅ Para usar el usuario correctamente

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.PositiveIntegerField(default=0)

    DURACION_CHOICES = [
        (30, "30 minutos"),
        (60, "1 hora"),
        (90, "1 hora y media"),
        (120, "2 horas"),
    ]
    duracion = models.PositiveSmallIntegerField(choices=DURACION_CHOICES, default=60)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.CharField(max_length=120)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estilista = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    fecha = models.DateField()
    hora = models.TimeField()

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.servicio} - {self.fecha} {self.hora}"
