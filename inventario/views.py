from django.shortcuts import render, redirect
from .models import Producto

def inventario(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/inventario.html', {'productos': productos})

def agregar_producto_form(request):
    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST.get('descripcion', ''),
            tipo=request.POST.get('tipo', 'venta'),
            precio=request.POST['precio'],
            stock=request.POST['stock'],
            stock_minimo=request.POST.get('stock_minimo', 5),
            codigo_barra=request.POST['codigo_barra'],
            unidad=request.POST.get('unidad', 'und'),
            imagen=request.FILES.get('imagen')
        )
        return redirect('inventario')  # ✅ vuelve al inventario

    return render(request, 'inventario/agregar_producto.html')
