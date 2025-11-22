from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils.timezone import localdate
from agenda.models import Servicio
from inventario.models import Producto
from .models import Venta, Gasto   # 👈 importa modelos financieros

# =====================================================
# DASHBOARD FINANZAS
# =====================================================
def finanzas(request):
    hoy = localdate()

    # Ingresos y gastos de HOY
    ingresos_hoy = Venta.objects.filter(fecha__date=hoy).aggregate(
        total=Sum("total")
    )["total"] or 0

    gastos_hoy = Gasto.objects.filter(fecha__date=hoy).aggregate(
        total=Sum("monto")
    )["total"] or 0

    ganancia_neta = ingresos_hoy - gastos_hoy

    if ingresos_hoy > 0:
        margen = round(ganancia_neta / ingresos_hoy * 100, 1)
    else:
        margen = 0

    # Transacciones recientes (HOY)
    transacciones = []

    for v in Venta.objects.filter(fecha__date=hoy).order_by("-fecha")[:10]:
        transacciones.append({
            "tipo": "ingreso",
            "titulo": "Venta en caja",
            "detalle": f"Método: {v.metodo_pago}",
            "monto": v.total,
            "fecha": v.fecha,
        })

    for g in Gasto.objects.filter(fecha__date=hoy).order_by("-fecha")[:10]:
        transacciones.append({
            "tipo": "gasto",
            "titulo": g.descripcion or "Gasto",
            "detalle": g.categoria or "",
            "monto": g.monto,
            "fecha": g.fecha,
        })

    # Ordenamos todo junto por fecha descendente
    transacciones = sorted(transacciones, key=lambda x: x["fecha"], reverse=True)

    context = {
        "ingresos_hoy": ingresos_hoy,
        "gastos_hoy": gastos_hoy,
        "ganancia_neta": ganancia_neta,
        "margen": margen,
        "transacciones": transacciones,
    }

    return render(request, "finanzas/finanzas.html", context)