from django.contrib import admin
from .models import SolicitudRetiro, Perfil
from django.contrib.auth.models import User
from django import forms

class SolicitudAdminForm(forms.ModelForm):
    class Meta:
        model = SolicitudRetiro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar para que solo muestre usuarios que estén en el grupo "Operario"
        self.fields['operario_asignado'].queryset = User.objects.filter(groups__name='Operario')

@admin.register(SolicitudRetiro)
class SolicitudRetiroAdmin(admin.ModelAdmin):
    form = SolicitudAdminForm
    list_display = ('ciudadano', 'material', 'estado', 'operario_asignado', 'fecha_estimada')
    list_filter = ('estado', 'material', 'operario_asignado')
    search_fields = ('ciudadano__username', 'operario_asignado__username')
    list_editable = ('operario_asignado',)