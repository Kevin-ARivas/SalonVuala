from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pagina_inicio'),
    path('servicios/', views.servicios, name='pagina_servicios'),
    path('matias/', views.matias, name='pagina_matias'),
    path('productos/', views.productos, name='pagina_productos'),
    path('reservar/', views.reservar, name='pagina_reservar'),
    path('reservar/exito/', views.exito, name='exito'),
]
