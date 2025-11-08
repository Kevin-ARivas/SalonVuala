from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_usuario, name='login_usuario'),
    path('logout/', logout_usuario, name='logout_usuario'),
    path('registro/', crear_usuario, name='registro_usuario'),
]