from django.shortcuts import render, redirect, get_object_or_404
from inventario.models import Producto
from agenda.models import Servicio, Cita
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from .models import Venta, DetalleVenta
from finanzas.models import MovimientoCaja

User = get_user_model()

# ---------------------------------------
#   FUNCIONES UTILES
# ---------------------------------------

def get_carrito(request):
    return request.session.get("carrito", [])

def save_carrito(request, carrito):
    request.session["carrito"] = carrito
    request.session.modified = True


# ---------------------------------------
#   VISTAS
# ---------------------------------------

def caja(request):
    carrito = get_carrito(request)
    total = sum(item["precio"] for item in carrito)

    return render(request, "ventas/caja.html", {
        "servicios": Servicio.objects.all(),
        "productos": Producto.objects.all(),
        "carrito": carrito,
        "total": total,
        "estilistas": User.objects.filter(tipo_usuario="estilista")
    })


def agregar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)

    carrito = get_carrito(request)
    carrito.append({
        "nombre": servicio.nombre,
        "precio": servicio.precio,
        "tipo": "servicio",
        "id": id
    })
    save_carrito(request, carrito)

    return redirect("caja")


def agregar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    carrito = get_carrito(request)
    carrito.append({
        "nombre": producto.nombre,
        "precio": producto.precio,
        "tipo": "producto",
        "id": id
    })
    save_carrito(request, carrito)

    # ❌ YA NO SE DESCUENTA STOCK AQUÍ

    return redirect("caja")


def eliminar_item(request, index):
    carrito = get_carrito(request)

    if 0 <= index < len(carrito):
        carrito.pop(index)

    save_carrito(request, carrito)
    return redirect("caja")


@transaction.atomic
def finalizar_venta(request):
    if request.method != "POST":
        return redirect("caja")

    carrito = get_carrito(request)

    if not carrito:
        messages.error(request, "El ticket está vacío.")
        return redirect("caja")

    total = sum(item["precio"] for item in carrito)
    estilista_id = request.POST.get("estilista")
    metodo = request.POST.get("metodo")

    estilista = User.objects.get(id=estilista_id) if estilista_id else None

    # 1️⃣ Crear la venta
    venta = Venta.objects.create(
        total=total,
        metodo_pago=metodo,
        fecha=timezone.now(),
        estilista=estilista
    )

    # 2️⃣ Crear detalle de venta y descontar stock
    for item in carrito:
        if item["tipo"] == "producto":
            producto = Producto.objects.get(id=item["id"])

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                precio=item["precio"],
                cantidad=1
            )

            producto.stock -= 1
            producto.save()

        else:
            servicio = Servicio.objects.get(id=item["id"])

            DetalleVenta.objects.create(
                venta=venta,
                servicio=servicio,
                precio=item["precio"],
                cantidad=1
            )

    # 3️⃣ Registrar ingreso en finanzas
    MovimientoCaja.objects.create(
        tipo="INGRESO",
        monto=venta.total,
        descripcion=f"Venta #{venta.id}",
        venta=venta
    )

    # 4️⃣ Limpiar carrito
    save_carrito(request, [])

    messages.success(request, "Venta registrada con éxito.")
    return redirect("caja")
