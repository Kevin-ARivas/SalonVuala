from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from inventario.models import Producto
from agenda.models import Servicio, Cita
from .models import Sucursales
from agenda.views import obtener_horas, generar_horas
import datetime



def index(request):
    return render(request, 'pagina_principal/index.html')

def servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'pagina_principal/servicios.html', {'servicios': servicios})

def matias(request):
    return render(request, 'pagina_principal/matias.html')

def productos(request):
    lista = Producto.objects.filter(tipo="venta")  # Solo los que se venden en front
    return render(request, 'pagina_principal/productos.html', {"productos": lista})

def exito(request):
    return render(request, 'pagina_principal/exito.html')


def reservar(request):
    servicios = Servicio.objects.all()
    sucursales = Sucursales.objects.all()
    
    #----FALTA LOGICA PARA LA VALIDACION DE HORAS Y FECHA, YO CAMBIARIA UN POCO EL TEMPLATE COMO EL DE ADMIN (QUIZAS QUEDA MAS FACIL)----
    
    pass
