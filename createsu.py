from django.contrib.auth import get_user_model
from django.core.management import execute_from_command_line
import django, os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SalonVuala.settings")
django.setup()

User = get_user_model()

username = "admin"
password = "admin123"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuario creado!")
else:
    print("El superusuario ya existe")
