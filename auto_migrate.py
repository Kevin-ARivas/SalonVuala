import os
import django
from django.core.management import call_command
from django.contrib.auth import get_user_model

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SalonVuala.settings')
django.setup()

print("📦 Ejecutando migraciones en Railway...")
call_command('makemigrations', interactive=False)
call_command('migrate', interactive=False)
print("✅ Migraciones completadas correctamente.")

# Crear superusuario automáticamente
User = get_user_model()
username = "Drumontt"
email = ""
password = "1234"  # ⚠️ Puedes cambiarla luego en /admin

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"👑 Superusuario '{username}' creado correctamente.")
else:
    print(f"✅ El superusuario '{username}' ya existe.")

print("🚀 Configuración completada.")
