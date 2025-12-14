from django.db import models
from django.conf import settings  # ✅ Para usar el usuario correctamente
from pagina_principal.models import Sucursales
from usuarios.models import Usuarios

def generar_duracion_horas():
    choices = []
    for minutos in range(30, 601, 30): 
        horas = minutos // 60
        mins_restantes = minutos % 60

        if horas == 0:
            texto = f"{mins_restantes} minutos"
        elif mins_restantes == 0:
            texto = f"{horas} hora" if horas == 1 else f"{horas} horas"
        else:
            texto = f"{horas} hora {mins_restantes} min" if horas == 1 else f"{horas} horas {mins_restantes} min"
        choices.append((minutos, texto))

    return choices

duracion_choices = generar_duracion_horas()

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.PositiveIntegerField(default=0)

    duracion = models.IntegerField(choices=duracion_choices)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        Usuarios,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='citas_cliente'
    )
    telefono = models.CharField(max_length=20, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, blank=True, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    estilista = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='citas_estilista'
    )

    fecha = models.DateField()
    hora = models.TimeField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.servicio} - {self.fecha} {self.hora}"
