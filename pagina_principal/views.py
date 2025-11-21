from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  
from inventario.models import Producto
from agenda.models import Servicio, Cita
from .models import Sucursales
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from usuarios.models import Usuarios


def index(request):
    return render(request, 'pagina_principal/index.html')

def servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'pagina_principal/servicios.html', {'servicios': servicios})

def matias(request):
    return render(request, 'pagina_principal/matias.html')

def productos(request):
    lista = Producto.objects.filter(tipo="venta")  # Solo los que se venden en front
    return render(request, 'pagina_principal/productos.html', {"productos": lista})

def exito(request, cita_id):
    cita = Cita.objects.get(id=cita_id)
    return render(request, 'pagina_principal/exito.html', {'cita': cita})


def horas_disponibles(request):
    sucursal_id = request.GET.get("sucursal_id")
    servicio_id = request.GET.get("servicio_id")
    fecha = request.GET.get("fecha")

    sucursal = Sucursales.objects.get(id=sucursal_id)
    servicio = Servicio.objects.get(id=servicio_id)

    duracion = timedelta(minutes=servicio.duracion)  # duración en minutos
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()

    # Horario de la peluquería
    hora_inicio = datetime.combine(fecha_dt, datetime.strptime("10:00", "%H:%M").time())
    hora_fin = datetime.combine(fecha_dt, datetime.strptime("20:00", "%H:%M").time())

    horas_posibles = []
    actual = hora_inicio

    while actual + duracion <= hora_fin:
        horas_posibles.append(actual.strftime("%H:%M"))
        actual += timedelta(minutes=30)

    # Ocupados en esa sucursal (pendientes y confirmados)
    citas_ocupadas = Cita.objects.filter(
        sucursal=sucursal,
        fecha=fecha,
        estado__in=["pendiente", "confirmada"]
    )

    horas_no_disponibles = set()

    for cita in citas_ocupadas:
        inicio = datetime.combine(fecha_dt, cita.hora)
        fin = inicio + timedelta(minutes=cita.servicio.duracion)

        # Bloquear todos los intervalos que se crucen
        actual = inicio
        while actual < fin:
            horas_no_disponibles.add(actual.strftime("%H:%M"))
            actual += timedelta(minutes=30)

    horas_libres = [h for h in horas_posibles if h not in horas_no_disponibles]

    return JsonResponse({"horas": horas_libres})
User = get_user_model()

@login_required
def reservar(request):
    if request.method == "POST":
        sucursal_id = request.POST.get("sucursal_id")
        servicio_id = request.POST.get("servicio_id")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        telefono = request.POST.get("telefono")

        # Validación básica
        if not (sucursal_id and servicio_id and fecha and hora):
            messages.error(request, "Faltan datos para crear la cita.")
            return redirect("reservar")

        sucursal = Sucursales.objects.get(id=sucursal_id)
        servicio = Servicio.objects.get(id=servicio_id)

        # El cliente SIEMPRE es el usuario logeado
        cliente = request.user

        # Selecciona un estilista disponible (usuario tipo trabajador)
        estilista = Usuarios.objects.filter(tipo_usuario='trabajador').first()

        # Validación de horario ocupado
        conflicto = Cita.objects.filter(
            sucursal=sucursal,
            fecha=fecha,
            hora=hora,
            estado__in=['pendiente', 'confirmada']
        ).exists()

        if conflicto:
            messages.error(request, "La hora seleccionada ya está ocupada.")
            return redirect("reservar")

        # Crear la cita
        cita = Cita.objects.create(
            cliente=cliente,
            telefono=telefono or cliente.telefono,   # si está vacío, usar el del usuario
            sucursal=sucursal,
            servicio=servicio,
            estilista=estilista,
            fecha=fecha,
            hora=hora,
        )

        messages.success(request, "Tu cita fue creada con éxito.")
        return redirect("exito", cita_id=cita.id)

    # GET: mostrar formulario
    sucursales = Sucursales.objects.all()
    servicios = Servicio.objects.all()

    return render(request, "pagina_principal/reservar.html", {
        "sucursales": sucursales,
        "servicios": servicios,
    })