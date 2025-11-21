from django.shortcuts import render, redirect, get_object_or_404
from agenda.models import Servicio, Cita
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime, time
from django.http import JsonResponse
from .forms import ServicioForm

User = get_user_model()


# ======================================================
#   📅 VISTA PRINCIPAL DE CITAS + CALENDARIO SEMANAL
# ======================================================
@login_required
def citas(request):

    # FECHA SEGURA
    fecha_str = request.GET.get("fecha")
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else date.today()
    except:
        fecha = date.today()

    # SEMANA SHIFT
    shift = int(request.GET.get("semana", 0))
    fecha = fecha + timedelta(days=7 * shift)

    # SEMANA LUN → DOM
    inicio_semana = fecha - timedelta(days=fecha.weekday())
    semana = [inicio_semana + timedelta(days=i) for i in range(7)]

    # FILTRO ESTILISTA
    estilista_id = request.GET.get('estilista')

    citas = Cita.objects.filter(fecha=fecha)
    if estilista_id:
        citas = citas.filter(estilista_id=estilista_id)

    total = citas.count()
    confirmadas = citas.filter(estado='confirmada').count()
    pendientes = citas.filter(estado='pendiente').count()

    citas_por_dia = {
        d: Cita.objects.filter(fecha=d).count()
        for d in semana
    }

    return render(request, 'agenda/citas.html', {
        "fecha": fecha,
        "hoy": date.today(),
        "semana": semana,
        "citas": citas,
        "estilistas": User.objects.filter(is_active=True),
        "citas_por_dia": citas_por_dia,
        "total": total,
        "confirmadas": confirmadas,
        "pendientes": pendientes
    })


# ======================================================
#   CRUD SERVICIOS
# ======================================================

@login_required
def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'agenda/servicios.html', {'servicios': servicios})


@login_required
def agregar_servicio(request):
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_servicios")
    else:
        form = ServicioForm()

    return render(request, "agenda/agregar_servicio.html", {"form": form})


@login_required
def editar_servicio(request, id):
    servicio = get_object_or_404(Servicio, pk=id)

    if request.method == "POST":
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect("lista_servicios")
    else:
        form = ServicioForm(instance=servicio)

    return render(request, "agenda/editar_servicio.html", {"form": form})


@login_required
def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect('lista_servicios')


# ======================================================
#   ✨ NUEVA CITA
# ======================================================
def generar_horas(duracion, citas_existentes):
    inicio = time(10, 0)
    fin    = time(20, 0)

    horas = []
    actual = datetime.combine(datetime.today(), inicio)
    limite = datetime.combine(datetime.today(), fin)

    while actual <= limite:
        hora_actual = actual.time()  # 👈 AHORA ES OBJETO time()

        ocupada = False
        for cita in citas_existentes:
            fin_cita_dt = datetime.combine(datetime.today(), cita.hora) + timedelta(minutes=cita.servicio.duracion)
            fin_cita = fin_cita_dt.time()

            if cita.hora <= hora_actual < fin_cita:
                ocupada = True
                break

        if not ocupada:
            horas.append(hora_actual)  # 👈 SE GUARDA COMO time(), NO STRING

        actual += timedelta(minutes=duracion)

    return horas

@login_required
def obtener_horas(request):
    servicio_id = request.GET.get("servicio")
    estilista_id = request.GET.get("estilista")
    fecha = request.GET.get("fecha")

    if not servicio_id or not estilista_id or not fecha:
        return JsonResponse({"horas": []})

    servicio = Servicio.objects.get(id=servicio_id)

    citas_existentes = Cita.objects.filter(
        fecha=fecha,
        estilista_id=estilista_id
    )

    horas = generar_horas(servicio.duracion, citas_existentes)

    # 👇 AQUÍ OCURRÍA TU ERROR
    horas_str = [h.strftime("%H:%M") for h in horas]  

    return JsonResponse({"horas": horas_str})

@login_required
def nueva_cita(request):
    servicios = Servicio.objects.all()
    estilistas = User.objects.filter(is_active=True)

    if request.method == "POST":

        # ⛔ VALIDAR FECHA NO ANTERIOR A HOY
        fecha = datetime.strptime(request.POST["fecha"], "%Y-%m-%d").date()
        if fecha < date.today():
            return render(request, "agenda/nueva_cita.html", {
                "servicios": servicios,
                "estilistas": estilistas,
                "error": "No puedes agendar citas en días anteriores."
            })

        Cita.objects.create(
            cliente       = request.POST["cliente"],
            telefono      = request.POST["telefono"],
            servicio_id   = request.POST["servicio"],
            estilista_id  = request.POST["estilista"],
            fecha         = request.POST["fecha"],
            hora          = request.POST["hora"],
        )
        return redirect("citas")

    return render(request, "agenda/nueva_cita.html", {
        "servicios": servicios,
        "estilistas": estilistas,
    })

@login_required
def confirmar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.estado = "confirmada"
    cita.save()
    return redirect("citas")

@login_required
def editar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    servicios = Servicio.objects.all()
    estilistas = User.objects.filter(is_active=True)

    if request.method == "POST":
        cita.cliente = request.POST["cliente"]
        cita.telefono = request.POST["telefono"]
        cita.servicio_id = request.POST["servicio"]
        cita.estilista_id = request.POST["estilista"]
        cita.fecha = request.POST["fecha"]
        cita.hora = request.POST["hora"]
        cita.save()
        return redirect("citas")

    return render(request, "agenda/editar_cita.html", {
        "cita": cita,
        "servicios": servicios,
        "estilistas": estilistas,
    })

@login_required
def eliminar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.delete()
    return redirect("citas")

@login_required
def pendiente_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.estado = "pendiente"
    cita.save()
    return redirect("citas")