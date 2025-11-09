"""
URL configuration for SalonVuala project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('citas/', views.citas, name='citas'),
    path('citas/nueva/', views.nueva_cita, name='nueva_cita'),

    # CRUD SERVICIOS
    path('servicios/', views.lista_servicios, name='lista_servicios'),
    path('servicios/agregar/', views.agregar_servicio, name='agregar_servicio'),
    path('servicios/editar/<int:id>/', views.editar_servicio, name='editar_servicio'),
    path('servicios/eliminar/<int:id>/', views.eliminar_servicio, name='eliminar_servicio'),
]

