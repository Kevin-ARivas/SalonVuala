from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios

@admin.register(Usuarios)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'telefono', 'tipo_usuario', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'telefono')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {"fields": ("telefono", "tipo_usuario")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Información adicional", {"fields": ("telefono", "tipo_usuario")}),
    )
