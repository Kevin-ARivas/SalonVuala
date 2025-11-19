from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
import requests
from .models import Usuarios
from .forms import UsuarioForm, UsuarioFormAdmin


# ============================================================
# 🔹 LISTAR USUARIOS
# ============================================================

def listar_usuarios(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})


# ============================================================
# 🔹 REGISTRO DE USUARIO + ENVÍO DE CORREO
# ============================================================

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_active = True              # cuenta activa para login si verificas después
            usuario.is_verified = False           # pero NO verificado
            usuario.save()

            # Enviar correo
            enviar_correo_verificacion(request, usuario)

            return render(request, "usuarios/registro_exitoso.html", {
                "email": usuario.email
            })

    else:
        form = UsuarioForm()

    return render(request, 'usuarios/registro.html', {'form': form})


# ============================================================
# 🔹 FUNCIÓN: ENVÍA CORREO DE VERIFICACIÓN
# ============================================================

def enviar_correo_verificacion(request, usuario):
    dominio = request.get_host()
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    token = default_token_generator.make_token(usuario)

    link_activacion = f"https://{dominio}/usuarios/activar/{uid}/{token}/"

    asunto = "Verifica tu cuenta en Salón Vualá"

    mensaje = f"""Hola {usuario.username}, verifica tu cuenta en el siguiente enlace:{link_activacion}"""

    return requests.post(
        f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={
            "from": settings.MAILGUN_FROM,
            "to": [usuario.email],
            "subject": asunto,
            "text": mensaje,
        }
    )



# ============================================================
# 🔹 ACTIVAR CUENTA DESDE CORREO
# ============================================================

def activar_cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuarios.objects.get(pk=uid)
    except:
        usuario = None

    if usuario and default_token_generator.check_token(usuario, token):
        usuario.is_verified = True
        usuario.save()
        return render(request, "usuarios/verificado.html")

    return render(request, "usuarios/verificado_invalido.html")


# ============================================================
# 🔹 EDITAR USUARIO
# ============================================================

def editar_usuario(request, pk):
    usuario = Usuarios.objects.get(pk=pk)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')

    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuarios/editar_usuario.html', {'form': form})


# ============================================================
# 🔹 ELIMINAR USUARIO
# ============================================================

def eliminar_usuario(request, pk):
    usuario = Usuarios.objects.get(pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})


# ============================================================
# 🔹 LOGIN SEGURO
# ============================================================

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        usuario = authenticate(request, username=username, password=password)

        if usuario is None:
            return render(request, 'usuarios/login.html', {
                'error': 'Credenciales inválidas'
            })

        # Bloquear login si no verificó correo
        if not usuario.is_verified:
            return render(request, 'usuarios/login.html', {
                'error': 'Debes verificar tu correo antes de ingresar.'
            })

        # Login normal
        login(request, usuario)

        if usuario.tipo_usuario == 'admin':
            return redirect('dashboard')

        return redirect('pagina_inicio')

    return render(request, 'usuarios/login.html')


# ============================================================
# 🔹 LOGOUT
# ============================================================

def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')
