from django.urls import path
from . import views

urlpatterns = [
    path("caja/", views.caja, name="caja"),
    path("agregar_servicio/<int:id>/", views.agregar_servicio, name="agregar_servicio"),
    path("agregar_producto/<int:id>/", views.agregar_producto, name="agregar_producto"),
    path("eliminar_item/<int:index>/", views.eliminar_item, name="eliminar_item"),
    path("finalizar/", views.finalizar_venta, name="finalizar_venta"),
]
