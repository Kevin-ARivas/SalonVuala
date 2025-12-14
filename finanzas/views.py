from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import localdate
from .models import Gasto
from ventas.models import Venta   # 👈 IMPORTANTE: importar Venta desde ventas

# =====================================================
# DASHBOARD FINANZAS
# =====================================================
def finanzas(request):
    hoy = localdate()

    # Ingresos y gastos de HOY
    ingresos_hoy = Venta.objects.filter(
        fecha__date=hoy
    ).aggregate(total=Sum("total"))["total"] or 0

    gastos_hoy = Gasto.objects.filter(
        fecha__date=hoy
    ).aggregate(total=Sum("monto"))["total"] or 0

    ganancia_neta = ingresos_hoy - gastos_hoy

    margen = round((ganancia_neta / ingresos_hoy) * 100, 1) if ingresos_hoy else 0

    # Transacciones recientes
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

    transacciones = sorted(
        transacciones,
        key=lambda x: x["fecha"],
        reverse=True
    )

    context = {
        "ingresos_hoy": ingresos_hoy,
        "gastos_hoy": gastos_hoy,
        "ganancia_neta": ganancia_neta,
        "margen": margen,
        "transacciones": transacciones,
    }

    return render(request, "finanzas/finanzas.html", context)
