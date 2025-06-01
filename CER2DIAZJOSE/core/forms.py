from django import forms
from django.contrib.auth.models import User
from .models import Perfil
from .models import SolicitudRetiro

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    direccion = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            perfil = user.perfil
            perfil.direccion = self.cleaned_data['direccion']
            perfil.telefono = self.cleaned_data['telefono']
            perfil.save()
        return user
    
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = SolicitudRetiro
        fields = ['material', 'cantidad', 'fecha_estimada']
        widgets = {
            'fecha_estimada': forms.DateInput(attrs={'type': 'date'}),
        }
class SolicitudOperarioForm(forms.ModelForm):
    class Meta:
        model = SolicitudRetiro
        fields = ['estado', 'comentario_operario']
