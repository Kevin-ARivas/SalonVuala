from django.shortcuts import render

# Create your views here.
def citas(request):
    return render(request, 'agenda/citas.html')