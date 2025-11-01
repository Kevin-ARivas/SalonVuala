from django.shortcuts import render, redirect
from .models import Servicio

def agregar_servicio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        Servicio.objects.create(nombre=nombre, precio=precio)
        return redirect('caja')

    return render(request, 'configuracion/agregar_servicio.html')