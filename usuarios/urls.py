from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.crear_usuario, name='registro_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Activación por correo:
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
]