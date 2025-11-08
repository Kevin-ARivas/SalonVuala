from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'pagina_principal/index.html')

def servicios(request):
    return render(request, 'pagina_principal/servicios.html')

def matias(request):
    return render(request, 'pagina_principal/matias.html')

def productos(request):
    return render(request, 'pagina_principal/productos.html')


def reservar(request):
    """
    Página pública de reserva con 1 sucursal (Río Bueno) y pasos:
    1) Sucursal 2) Servicio 3) Fecha/Hora 4) Datos 5) Confirmación
    """
    servicios = [
        {"id": 1, "nombre": "Corte mujer", "duracion": 45, "precio": 12000},
        {"id": 2, "nombre": "Corte hombre", "duracion": 30, "precio": 8000},
        {"id": 3, "nombre": "Color raíz", "duracion": 90, "precio": 25000},
        {"id": 4, "nombre": "Balayage", "duracion": 150, "precio": 60000},
        {"id": 5, "nombre": "Peinado evento", "duracion": 60, "precio": 20000},
        {"id": 6, "nombre": "Tratamiento capilar", "duracion": 45, "precio": 15000},
    ]
    contexto = {
        "sucursal": {
            "nombre": "Salón Vualá — Río Bueno",
            "direccion": "Oriente 1078, Río Bueno",
            "telefono": "+56 9 0000 0000",
        },
        "servicios": servicios
    }
    return render(request, 'pagina_principal/reservar.html', contexto)


@csrf_exempt
def reservar_enviar(request):
    if request.method == "POST":
        datos = {
            "sucursal": request.POST.get("sucursal"),
            "servicio": request.POST.get("servicio"),
            "fecha": request.POST.get("fecha"),
            "hora": request.POST.get("hora"),
            "nombre": request.POST.get("nombre"),
            "email": request.POST.get("email"),
            "telefono": request.POST.get("telefono"),
            "comentarios": request.POST.get("comentarios"),
        }
        return render(request, 'pagina_principal/reserva_ok.html', {"datos": datos})

    return redirect('/reservar/')
