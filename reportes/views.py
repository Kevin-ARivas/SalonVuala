from django.shortcuts import render
from django.utils.timezone import localdate
from django.db.models import Sum, Count
from agenda.models import Cita
from ventas.models import Venta, DetalleVenta

def reportes_dashboard(request):
    hoy = localdate()

    # -----------------------------
    # Citas confirmadas hoy (solo informativo)
    # -----------------------------
    citas_hoy = Cita.objects.filter(
        fecha=hoy,
        estado="confirmada"
    )

    # -----------------------------
    # Ventas reales del día
    # -----------------------------
    ventas_hoy = Venta.objects.filter(
        fecha__date=hoy
    )

    ingresos_totales = ventas_hoy.aggregate(
        total=Sum("total")
    )["total"] or 0

    # -----------------------------
    # Servicios realizados (desde caja)
    # -----------------------------
    servicios_realizados = DetalleVenta.objects.filter(
        venta__fecha__date=hoy,
        servicio__isnull=False
    ).count()

    # -----------------------------
    # Productos vendidos (desde caja)
    # -----------------------------
    productos_vendidos = DetalleVenta.objects.filter(
        venta__fecha__date=hoy,
        producto__isnull=False
    ).aggregate(total=Sum("cantidad"))["total"] or 0

    # -----------------------------
    # Clientes únicos (ventas del día)
    # -----------------------------
    clientes_unicos = ventas_hoy.exclude(
        estilista__isnull=True
    ).values("estilista").distinct().count()

    return render(request, "reportes/reportes.html", {
        "citas_hoy": citas_hoy,
        "ingresos_totales": ingresos_totales,
        "servicios_realizados": servicios_realizados,
        "productos_vendidos": productos_vendidos,
        "clientes_unicos": clientes_unicos,
    })
