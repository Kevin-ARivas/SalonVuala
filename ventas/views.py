from django.shortcuts import render, redirect, get_object_or_404
from inventario.models import Producto
from agenda.models import Servicio, Cita
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from .models import Venta

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

    # descontar stock
    producto.stock -= 1
    producto.save()

    return redirect("caja")


def eliminar_item(request, index):
    carrito = get_carrito(request)

    if 0 <= index < len(carrito):
        carrito.pop(index)

    save_carrito(request, carrito)
    return redirect("caja")


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

    # Crear la venta
    Venta.objects.create(
        total=total,
        metodo_pago=metodo,
        fecha=timezone.now(),
        estilista=estilista
    )

    # Limpiar carrito
    save_carrito(request, [])

    messages.success(request, "Venta registrada con éxito.")
    return redirect("caja")
