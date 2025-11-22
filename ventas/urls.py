from django.urls import path
from . import views

urlpatterns = [
    path('caja/', views.caja, name='caja'),
    path('agregar-servicio/<int:id>/', views.agregar_servicio, name='agregar_servicio'),
    path('agregar-producto/<int:id>/', views.agregar_producto, name='agregar_producto'),
    path('finalizar-venta/', views.finalizar_venta, name='finalizar_venta'),
]
