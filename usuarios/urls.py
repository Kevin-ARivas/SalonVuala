from django.urls import path
from . import views
import include

urlpatterns = [
    path('registro/', views.crear_usuario, name='registro_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),

# Google OAuth (lo maneja social_django)
    path('', include('social_django.urls', namespace='social')),
]