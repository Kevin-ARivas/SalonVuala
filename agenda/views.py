from django.shortcuts import render, redirect, get_object_or_404
from agenda.models import Servicio, Cita
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import date

User = get_user_model()
# -----------------------------
#   CITAS (Vista principal)
# -----------------------------

@login_required
def citas(request):
    # Obtener fecha seleccionada, si no usar la de hoy
    fecha = request.GET.get('fecha', date.today())

    # Obtener estilista seleccionado (si existe)
    estilista_id = request.GET.get('estilista')

    # Obtener lista completa de estilistas
    estilistas = User.objects.filter(is_active=True)

    # Filtrar citas por fecha
    citas = Cita.objects.filter(fecha=fecha)

    # Si seleccionó estilista, filtrar también
    if estilista_id:
        citas = citas.filter(estilista_id=estilista_id)

    # Contadores para resumen
    total = citas.count()
    confirmadas = citas.filter(estado='confirmada').count()
    pendientes = citas.filter(estado='pendiente').count()

    return render(request, 'agenda/citas.html', {
        'citas': citas,
        'estilistas': estilistas,
        'fecha': fecha,
        'total': total,
        'confirmadas': confirmadas,
        'pendientes': pendientes
    })

# -----------------------------
#   LISTA DE SERVICIOS (CRUD)
# -----------------------------
@login_required
def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'agenda/servicios.html', {'servicios': servicios})


# -----------------------------
#   CREAR SERVICIO
# -----------------------------
@login_required
def agregar_servicio(request):
    if request.method == 'POST':
        Servicio.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST.get('descripcion', ''),
            precio=request.POST['precio'],
            duracion=request.POST['duracion']
        )
        return redirect('lista_servicios')

    return render(request, 'agenda/agregar_servicio.html')


# -----------------------------
#   EDITAR SERVICIO
# -----------------------------
@login_required
def editar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)

    if request.method == 'POST':
        servicio.nombre = request.POST['nombre']
        servicio.descripcion = request.POST.get('descripcion', '')
        servicio.precio = request.POST['precio']
        servicio.duracion = request.POST['duracion']
        servicio.save()
        return redirect('lista_servicios')

    return render(request, 'agenda/editar_servicio.html', {'servicio': servicio})


# -----------------------------
#   ELIMINAR SERVICIO
# -----------------------------
@login_required
def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect('lista_servicios')



# ======================================================
#   🟣 CREAR NUEVA CITA
# ======================================================
@login_required
def nueva_cita(request):
    servicios = Servicio.objects.all()
    estilistas = User.objects.filter(is_active=True)  # ✅ Admin y trabajadores

    if request.method == 'POST':
        Cita.objects.create(
            cliente=request.POST['cliente'],
            telefono=request.POST['telefono'],
            servicio_id=request.POST['servicio'],
            estilista_id=request.POST['estilista'],
            fecha=request.POST['fecha'],
            hora=request.POST['hora'],
        )
        return redirect('citas')

    return render(request, 'agenda/nueva_cita.html', {
        'servicios': servicios,
        'estilistas': estilistas
    })

