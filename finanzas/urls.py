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
from . import views as inicio_views

urlpatterns = [
    path('', inicio_views.finanzas, name='finanzas'),
    path('caja/', views.caja, name='caja'),
    path('agregar-servicio/<int:id>/', views.agregar_servicio, name='agregar_servicio'),
    path('agregar-producto/<int:id>/', views.agregar_producto, name='agregar_producto'),
    path('finalizar-venta/', views.finalizar_venta, name='finalizar_venta'),
]
