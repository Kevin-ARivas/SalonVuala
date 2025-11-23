"""
Django settings for SalonVuala project.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()  # Para cargar .env localmente

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# 🔐 SEGURIDAD
# ============================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "salonvuala-production.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://salonvuala-production.up.railway.app"
]


# ============================================================
# 📦 APPS DEL PROYECTO
# ============================================================
INSTALLED_APPS = [
    # Apps tuyas
    'agenda',
    'configuracion',
    'finanzas',
    'inicio',
    'inventario',
    'proveedores',
    'reportes',
    'usuarios',
    'ventas',
    'pagina_principal',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Autenticación social
    'social_django',
]


# ============================================================
# 🧱 MIDDLEWARE
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# 🔐 AUTENTICACIÓN SOCIAL
# ============================================================
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True


# ============================================================
# 🔗 CONFIGURACIÓN DE BASE DE DATOS
# ============================================================

# Si existe DATABASE_URL -> PostgreSQL (Railway)
# Si NO existe -> SQLite local
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}


# ============================================================
# 📚 USER MODEL PERSONALIZADO
# ============================================================
AUTH_USER_MODEL = 'usuarios.Usuarios'


# ============================================================
# 🔐 VALIDACIÓN DE CONTRASEÑAS
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================
# 🌍 REGIONALIZACIÓN
# ============================================================
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# ============================================================
# 🖼️ STATIC Y MEDIA
# ============================================================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "pagina_principal" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ============================================================
# 📧 EMAIL (Mailgun)
# ============================================================
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
MAILGUN_FROM = os.environ.get("MAILGUN_FROM")


# ============================================================
# 🔧 DJANGO TEMPLATES
# ============================================================
ROOT_URLCONF = 'SalonVuala.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SalonVuala.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
