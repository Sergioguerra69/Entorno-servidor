from django import forms
from .models import Juego

class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre_sala']
        widgets = {
            'nombre_sala': forms.TextInput(attrs={
                'class': 'control-formulario',
                'placeholder': 'Ingresa el nombre de la sala'
            })
        }
    
    def clean_nombre_sala(self):
        nombre_sala = self.cleaned_data.get('nombre_sala')
        if Juego.objects.filter(nombre_sala=nombre_sala).exists():
            raise forms.ValidationError("Ya existe una sala con este nombre")
        return nombre_sala