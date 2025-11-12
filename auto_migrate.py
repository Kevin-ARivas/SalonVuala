import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SalonVuala.settings')
application = get_wsgi_application()

print("📦 Ejecutando migraciones en Railway...")
call_command('makemigrations', interactive=False)
call_command('migrate', interactive=False)
print("✅ Migraciones completadas correctamente.")
