from django.shortcuts import render, redirect, get_object_or_404
from inventario.models import Producto
from agenda.models import Servicio
from .models import Venta
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()

# CARRITO TEMPORAL
carrito = []

def caja(request):
    total = sum([i['precio'] for i in carrito])
    return render(request, 'ventas/caja.html', {
        'servicios': Servicio.objects.all(),
        'productos': Producto.objects.all(),
        'carrito': carrito,
        'total': total,
        'estilistas': User.objects.filter(tipo_usuario='estilista')
    })

def agregar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    carrito.append({
        'nombre': servicio.nombre,
        'precio': servicio.precio,
        'tipo': 'servicio',
        'id': id
    })
    return redirect('caja')

def agregar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    carrito.append({
        'nombre': producto.nombre,
        'precio': producto.precio,
        'tipo': 'producto',
        'id': id
    })

    # Descontar stock
    producto.stock -= 1
    producto.save()

    return redirect('caja')

def finalizar_venta(request):
    if request.method == "POST":
        metodo = request.POST.get("metodo")

        total = sum([item['precio'] for item in carrito])

        # Registrar venta real
        Venta.objects.create(
            total=total,
            metodo_pago=metodo,
            fecha=timezone.now()
        )

        # Vaciar carrito
        carrito.clear()

        return redirect('caja')

    return redirect('caja')
