from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Juego        

# Formulario para juegos
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

# Formulario para registro de usuarios
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Requerido. Introduce un email válido.'
    )
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user