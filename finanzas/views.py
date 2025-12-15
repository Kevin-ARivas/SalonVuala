from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import localdate
from .models import Gasto
from ventas.models import Venta
from django.contrib.auth.decorators import login_required

@login_required
def finanzas(request):
    hoy = localdate()
    user = request.user

    if user.tipo_usuario == "trabajador":
        ingresos_qs = Venta.objects.filter(
            fecha__date=hoy,
            estilista=user
        )
        gastos_qs = Gasto.objects.none()  # trabajador no ve gastos globales
    else:
        ingresos_qs = Venta.objects.filter(fecha__date=hoy)
        gastos_qs = Gasto.objects.filter(fecha__date=hoy)

    ingresos_hoy = ingresos_qs.aggregate(total=Sum("total"))["total"] or 0
    gastos_hoy = gastos_qs.aggregate(total=Sum("monto"))["total"] or 0

    ganancia_neta = ingresos_hoy - gastos_hoy
    margen = round((ganancia_neta / ingresos_hoy) * 100, 1) if ingresos_hoy else 0

    transacciones = []

    for v in ingresos_qs.order_by("-fecha")[:10]:
        transacciones.append({
            "tipo": "ingreso",
            "titulo": "Venta",
            "detalle": f"Método: {v.metodo_pago}",
            "monto": v.total,
            "fecha": v.fecha,
        })

    for g in gastos_qs.order_by("-fecha")[:10]:
        transacciones.append({
            "tipo": "gasto",
            "titulo": g.descripcion or "Gasto",
            "detalle": g.categoria or "",
            "monto": g.monto,
            "fecha": g.fecha,
        })

    transacciones = sorted(transacciones, key=lambda x: x["fecha"], reverse=True)

    return render(request, "finanzas/finanzas.html", {
        "ingresos_hoy": ingresos_hoy,
        "gastos_hoy": gastos_hoy,
        "ganancia_neta": ganancia_neta,
        "margen": margen,
        "transacciones": transacciones,
    })
