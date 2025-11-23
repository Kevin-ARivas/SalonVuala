from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ["nombre", "descripcion", "precio", "duracion"]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 shadow-sm focus:ring-pink-500 focus:border-pink-500 transition-all"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "w-full rounded-lg border border-gray-300 shadow-sm focus:ring-pink-500 focus:border-pink-500 transition-all",
                "rows": 3
            }),
            "precio": forms.NumberInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 shadow-sm focus:ring-pink-500 focus:border-pink-500 transition-all ",
                "min": 0
            }),
            "duracion": forms.Select(attrs={
                "class": "w-full rounded-lg border border-gray-300 shadow-sm focus:ring-pink-500 focus:border-pink-500 transition-all "
            }),
        }
