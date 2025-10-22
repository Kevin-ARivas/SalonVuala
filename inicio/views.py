from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'inicio/dashboard.html')
    