from django.shortcuts import render
from django.utils.timezone import localdate
from django.db.models import Sum
from agenda.models import Cita
from ventas.models import Venta   # 👈 CLAVE

def reportes_dashboard(request):
    hoy = localdate()

    # Citas confirmadas hoy (solo informativo)
    citas_hoy = Cita.objects.filter(
        fecha=hoy,
        estado="confirmada"
    )

    # Ingresos reales desde caja (ventas)
    ingresos_totales = Venta.objects.filter(
        fecha__date=hoy
    ).aggregate(total=Sum("total"))["total"] or 0

    return render(request, "reportes/reportes.html", {
        "citas_hoy": citas_hoy,
        "ingresos_totales": ingresos_totales,
    })
