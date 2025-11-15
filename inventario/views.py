from django.shortcuts import render, redirect
from .models import Producto
from django.db.models import F


def inventario(request):
    productos = Producto.objects.all()

    # ====== FILTROS ======
    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()

    # 🔍 Filtro por nombre o descripción
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) |
            Q(descripcion__icontains=search)
        )

    # 🏷️ FILTRO REAL POR CATEGORÍA (el correcto)
    if category:
        productos = productos.filter(categoria=category)

    # ====== MÉTRICAS ======
    total_productos = productos.count()
    stock_bajo = productos.filter(stock__lte=F('stock_minimo')).count()
    valor_total = sum(p.precio * p.stock for p in productos)

    return render(request, 'inventario/inventario.html', {
        'productos': productos,
        'total_productos': total_productos,
        'stock_bajo': stock_bajo,
        'valor_total': valor_total,
        'search': search,
        'category': category,
    })

def agregar_producto_form(request):
    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST.get('descripcion', ''),
            tipo=request.POST.get('tipo', 'venta'),
            categoria=request.POST.get('categoria', 'shampoo'),   # ⭐ NUEVO
            precio=request.POST['precio'],
            stock=request.POST['stock'],
            stock_minimo=request.POST.get('stock_minimo', 5),
            codigo_barra=request.POST['codigo_barra'],
            unidad=request.POST.get('unidad', 'und'),
            imagen=request.FILES.get('imagen')
        )
        return redirect('inventario')

    return render(request, 'inventario/agregar_producto.html')

def editar_producto(request, id):
    producto = Producto.objects.get(id=id)

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST.get('descripcion', '')
        producto.tipo = request.POST.get('tipo', 'venta')
        producto.categoria = request.POST.get('categoria', 'otro')
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.stock_minimo = request.POST.get('stock_minimo', 5)
        producto.codigo_barra = request.POST['codigo_barra']
        producto.unidad = request.POST.get('unidad', 'und')

        if request.FILES.get('imagen'):
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('inventario')

    return render(request, 'inventario/editar_producto.html', {'producto': producto})

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)

    if request.method == "POST":
        producto.delete()
        return redirect('inventario')

    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})


