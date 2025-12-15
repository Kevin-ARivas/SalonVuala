from django.shortcuts import render
from django.core.paginator import Paginator
from agenda.models import Cita
from inventario.models import Producto
from ventas.models import Venta
from datetime import date
from django.db import models
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    hoy = date.today()
    user = request.user

    # =========================
    # FILTRO POR ROL
    # =========================
    if user.tipo_usuario == "trabajador":
        citas_hoy = Cita.objects.filter(fecha=hoy, estilista=user)
        ingresos_qs = Venta.objects.filter(fecha=hoy, estilista=user)
    else:
        citas_hoy = Cita.objects.filter(fecha=hoy)
        ingresos_qs = Venta.objects.filter(fecha=hoy)

    total_citas_hoy = citas_hoy.count()
    atendidas_hoy = citas_hoy.filter(estado="atendida").count()

    ingresos_hoy = ingresos_qs.aggregate(
        total=models.Sum("total")
    )["total"] or 0

    productos_bajos = Producto.objects.filter(
        stock__lte=models.F("stock_minimo")
    ).order_by("stock")

    productos = Producto.objects.all().order_by("nombre")
    paginator = Paginator(productos, 4)
    productos_page = paginator.get_page(request.GET.get("page"))

    return render(request, "inicio/dashboard.html", {
        "citas_hoy": citas_hoy,
        "total_citas_hoy": total_citas_hoy,
        "atendidas_hoy": atendidas_hoy,
        "ingresos_hoy": ingresos_hoy,
        "productos_bajos": productos_bajos,
        "productos_page": productos_page,
    })
