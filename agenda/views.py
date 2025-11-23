from django.shortcuts import render, redirect, get_object_or_404
from agenda.models import Servicio, Cita
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime, time
from django.http import JsonResponse
from .forms import ServicioForm
from usuarios.models import Usuarios
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q
import re
from django.contrib import messages

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

@require_GET
@login_required
def buscar_clientes(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'results': []})

    # 
    qs = Usuarios.objects.filter(#.filter(tipo_usuario='cliente')( #← FILTRAR SOLO CLIENTES
        Q(username__icontains=q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(rut__icontains=q) |
        Q(telefono__icontains=q)
    )[:12]  # limitar resultados

    results = []
    for u in qs:
        results.append({
            'id': u.id,
            'label': f"{u.first_name or u.username} {u.last_name or ''} — {u.rut or ''}",
            'name': u.first_name or u.username,
            'phone': u.telefono or '',
            'rut': u.rut or '',
        })
    return JsonResponse({'results': results})


@login_required
def nueva_cita(request):
    servicios = Servicio.objects.all()
    estilistas = Usuarios.objects.filter(tipo_usuario='trabajador', is_active=True)

    if request.method == "POST":
        # validar fecha
        fecha_str = request.POST.get("fecha")
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except Exception:
            return render(request, "agenda/nueva_cita.html", {
                "servicios": servicios,
                "estilistas": estilistas,
                "error": "Fecha inválida."
            })

        if fecha < date.today():
            return render(request, "agenda/nueva_cita.html", {
                "servicios": servicios,
                "estilistas": estilistas,
                "error": "No puedes agendar citas en días anteriores."
            })

        servicio_id = request.POST.get("servicio")
        estilista_id = request.POST.get("estilista")
        hora = request.POST.get("hora")

        # CLIENTE: preferimos id (cuando admin selecciona), sino creamos uno rápido
        cliente_id = request.POST.get("cliente")  # hidden input con id si se seleccionó
        cliente_nombre = request.POST.get("cliente_search", "").strip()
        cliente_telefono = request.POST.get("telefono", "").strip()
        cliente = None

        if cliente_id:
            try:
                cliente = Usuarios.objects.get(id=cliente_id)
            except Usuarios.DoesNotExist:
                cliente = None

        if not cliente:
            # Intentar encontrar por RUT o teléfono (evita duplicados)
            if cliente_telefono:
                cliente, created = Usuarios.objects.get_or_create(
                    telefono=cliente_telefono,
                    defaults={
                        'username': f"cli_{cliente_telefono}",
                        'first_name': cliente_nombre or cliente_telefono,
                        'tipo_usuario': 'cliente'
                    }
                )
            else:
                # Crear temp con username único
                base = (cliente_nombre or "cliente").strip().replace(" ", "_")[:20]
                username = f"{base}_{int(datetime.now().timestamp())}"
                cliente = Usuarios.objects.create(
                    username=username,
                    first_name=cliente_nombre or username,
                    tipo_usuario='cliente'
                )

        # crear cita
        Cita.objects.create(
            cliente=cliente,
            telefono=cliente_telefono or cliente.telefono,
            servicio_id=servicio_id,
            estilista_id=estilista_id,
            fecha=fecha,
            hora=hora
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

    # SOLO trabajadores o admins
    estilistas = Usuarios.objects.filter(
        is_active=True,
        tipo_usuario__in=["trabajador", "admin"]
    )

    if request.method == "POST":
        try:
            # ==========================
            # CLIENTE
            # ==========================
            cliente_id = request.POST.get("cliente_id")
            cita.cliente = Usuarios.objects.get(pk=cliente_id)

            # ==========================
            # TELÉFONO CHILENO
            # ==========================
            telefono = request.POST.get("telefono", "").strip()
            if telefono and not re.match(r"^(\+569\d{8}|9\d{8})$", telefono):
                return render(request, "agenda/editar_cita.html", {
                    "cita": cita, "servicios": servicios, "estilistas": estilistas,
                    "error": "📞 El teléfono debe ser +569XXXXXXXX o 9XXXXXXXX"
                })
            cita.telefono = telefono

            # ==========================
            # DATOS BÁSICOS
            # ==========================
            servicio_id = request.POST.get("servicio")
            estilista_id = request.POST.get("estilista")
            fecha_str = request.POST.get("fecha")
            hora_str = request.POST.get("hora")

            cita.servicio_id = servicio_id
            cita.estilista_id = estilista_id
            cita.fecha = fecha_str
            cita.hora = hora_str

            # ==========================
            # PREVENIR SOLAPAMIENTOS
            # ==========================
            nuevo_inicio = datetime.combine(
                datetime.strptime(fecha_str, "%Y-%m-%d"),
                datetime.strptime(hora_str, "%H:%M").time()
            )
            duracion = Servicio.objects.get(id=servicio_id).duracion
            nuevo_fin = nuevo_inicio + timedelta(minutes=duracion)

            citas_existentes = Cita.objects.filter(
                fecha=fecha_str,
                estilista_id=estilista_id
            ).exclude(id=cita.id)

            for c in citas_existentes:
                inicio = datetime.combine(c.fecha, c.hora)
                fin = inicio + timedelta(minutes=c.servicio.duracion)

                if inicio < nuevo_fin and nuevo_inicio < fin:
                    return render(request, "agenda/editar_cita.html", {
                        "cita": cita, "servicios": servicios, "estilistas": estilistas,
                        "error": "⚠ El estilista ya tiene una cita en ese horario."
                    })

            # ==========================
            # GUARDAR
            # ==========================
            cita.save()
            messages.success(request, "Cita actualizada correctamente.")
            return redirect("citas")

        except Usuarios.DoesNotExist:
            return render(request, "agenda/editar_cita.html", {
                "cita": cita, "servicios": servicios, "estilistas": estilistas,
                "error": "❌ El cliente no existe en el sistema."
            })

    # ==========================
    # GET NORMAL
    # ==========================
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



def get_or_create_cliente(nombre, telefono=None, rut=None):
    # Si viene rut → buscar por rut
    if rut:
        cliente = Usuarios.objects.filter(rut=rut).first()
        if cliente:
            return cliente

    # Si viene teléfono → buscar por teléfono
    if telefono:
        cliente = Usuarios.objects.filter(telefono=telefono).first()
        if cliente:
            return cliente

    # Crear nuevo si no existe ninguno
    return Usuarios.objects.create(
        username=f"cli_{telefono or rut or int(datetime.now().timestamp())}",
        first_name=nombre,
        tipo_usuario="cliente",
        telefono=telefono,
        rut=rut
    )