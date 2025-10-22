from django.shortcuts import render

# Create your views here.
def finanzas(request):
    return render(request, 'finanzas/finanzas.html')
