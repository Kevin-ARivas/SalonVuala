"""
URL configuration for SalonVuala project.
"""

from django.contrib import admin
from django.urls import path, include

# Para servir imágenes y estáticos en desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # *** Sitio Público ***
    path('', include('pagina_principal.urls')),   # Página web para clientes

    # *** Panel Administrativo Moderno (Dashboard Interno) ***
    path('inicio/', include('inicio.urls')),      # Dashboard del salón

    # *** Panel administrativo Django clásico ***
    path('admin/', admin.site.urls),

    # *** Apps internas del sistema ***
    path('agenda/', include('agenda.urls')),
    path('configuracion/', include('configuracion.urls')),
    path('finanzas/', include('finanzas.urls')),
    path('inventario/', include('inventario.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('reportes/', include('reportes.urls')),
    path('usuarios/', include('usuarios.urls')),
    
]

# ✅ Servir imágenes subidas en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ✅ Servir archivos estáticos en desarrollo
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
