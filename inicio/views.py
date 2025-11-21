# views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from agenda.models import Cita
from inventario.models import Producto
from finanzas.models import Venta
from datetime import date
from django.db import models

def dashboard(request):
    hoy = date.today()

    # Citas
    citas_hoy = Cita.objects.filter(fecha=hoy).order_by("hora")
    total_citas_hoy = citas_hoy.count()
    atendidas_hoy = citas_hoy.filter(estado="atendida").count()

    # Ingresos
    ingresos_hoy = Venta.objects.filter(fecha=hoy).aggregate(total=models.Sum("total"))["total"] or 0

    # Productos con stock bajo (para mostrar alertas)
    productos_bajos = Producto.objects.filter(stock__lte=models.F("stock_minimo")).order_by("stock")

    # Paginación inventario (TODOS LOS PRODUCTOS)
    productos = Producto.objects.all().order_by("nombre")
    paginator = Paginator(productos, 4)
    page_number = request.GET.get("page")
    productos_page = paginator.get_page(page_number)

    context = {
        "citas_hoy": citas_hoy,
        "total_citas_hoy": total_citas_hoy,
        "atendidas_hoy": atendidas_hoy,
        "ingresos_hoy": ingresos_hoy,
        "productos_bajos": productos_bajos,  # ← IMPORTANTE
        "productos_page": productos_page,    # ← PARA MOSTRAR 4 Y PAGINAR
    }

    return render(request, "inicio/dashboard.html", context)