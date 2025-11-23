


from django.shortcuts import render
from django.utils import timezone
from agenda.models import Cita
from django.db.models import Sum, F

def reportes_dashboard(request):
    hoy = timezone.now().date()

    citas_hoy = Cita.objects.filter(
        fecha=hoy,
        estado="confirmada"
    )

    # Ingresos = suma del precio del servicio asociado a cada cita confirmada
    ingresos_totales = citas_hoy.aggregate(
        total=Sum(F("servicio__precio"))
    )["total"] or 0

    return render(request, "reportes/reportes.html", {
        "citas_hoy": citas_hoy,
        "ingresos_totales": ingresos_totales,
    })

