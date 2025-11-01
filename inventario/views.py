from django.shortcuts import render, redirect
from .models import Producto

def inventario(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/inventario.html', {'productos': productos})

def agregar_producto_form(request):
    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST['nombre'],
            precio=request.POST['precio'],
            stock=request.POST['stock'],
            codigo_barra=request.POST['codigo_barra']
        )
        return redirect('caja')  # vuelve a caja después de agregar
    return render(request, 'inventario/agregar_producto.html')
