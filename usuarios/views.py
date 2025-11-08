from django.shortcuts import render, redirect
from .models import Usuarios
from .forms import UsuarioForm, UsuarioFormAdmin
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def listar_usuarios(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            return redirect('pagina_inicio')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def editar_usuario(request, pk):
    usuario = Usuarios.objects.get(pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

def eliminar_usuario(request, pk):
    usuario = Usuarios.objects.get(pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            print(usuario.tipo_usuario)
            if usuario.tipo_usuario == 'admin':
                login(request, usuario)
                print("Usuario admin ha iniciado sesión.")
                return redirect('dashboard')
            elif usuario.tipo_usuario == 'cliente':
                login(request, usuario)
                return redirect('pagina_inicio')
            elif usuario.tipo_usuario == 'trabajador':
                login(request, usuario)
                return redirect('pagina_inicio')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'usuarios/login.html')

def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')