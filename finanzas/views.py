from django.shortcuts import render, redirect
from configuracion.models import Servicio
from inventario.models import Producto

# Create your views here.
def finanzas(request):
    return render(request, 'finanzas/finanzas.html')

carrito = []

def caja(request):
    total = sum([i['precio'] for i in carrito])
    return render(request, 'finanzas/caja.html', {
        'servicios': Servicio.objects.all(),
        'productos': Producto.objects.all(),
        'carrito': carrito,
        'total': total,
    })

def agregar_servicio(request, id):
    servicio = Servicio.objects.get(id=id)
    carrito.append({'nombre': servicio.nombre, 'precio': servicio.precio})
    return redirect('caja')

def agregar_producto(request, id):
    producto = Producto.objects.get(id=id)
    carrito.append({'nombre': producto.nombre, 'precio': producto.precio})
    producto.stock -= 1
    producto.save()
    return redirect('caja')

def finalizar_venta(request):
    global carrito
    carrito = []
    return redirect('caja')