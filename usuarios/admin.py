from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios

@admin.register(Usuarios)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'rut',
        'email',
        'telefono',
        'tipo_usuario',
        'is_staff',
        'is_active',
        "is_verified",
    )

    search_fields = (
        'username',
        'rut',
        'email',
        'telefono'
    )

    list_filter = (
        'tipo_usuario',
        'is_staff',
        'is_active',
        "is_verified",
    )

    
    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {
            "fields": ("rut", "telefono", "tipo_usuario", "is_verified")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información adicional", {
            "fields": ("rut", "telefono", "tipo_usuario", "is_verified")
        }),
    )

