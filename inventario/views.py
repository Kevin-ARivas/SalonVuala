from django.shortcuts import render

# Create your views here.
def inventario(request):
    return render(request, 'inventario/inventario.html')
