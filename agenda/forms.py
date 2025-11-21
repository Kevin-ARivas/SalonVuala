from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ["nombre", "descripcion", "precio", "duracion"]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "w-full border-gray-300 focus:border-pink-500 focus:ring-pink-500 rounded-lg px-4 py-2"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "w-full border-gray-300 focus:border-pink-500 focus:ring-pink-500 rounded-lg px-4 py-2",
                "rows": 3
            }),
            "precio": forms.NumberInput(attrs={
                "class": "w-full border-gray-300 focus:border-pink-500 focus:ring-pink-500 rounded-lg px-4 py-2",
                "min": 0
            }),
            "duracion": forms.Select(attrs={
                "class": "w-full border-gray-300 focus:border-pink-500 focus:ring-pink-500 rounded-lg px-4 py-2"
            }),
        }
