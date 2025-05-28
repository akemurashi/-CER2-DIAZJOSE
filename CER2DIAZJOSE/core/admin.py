from django.contrib import admin
from .models import SolicitudRetiro

@admin.register(SolicitudRetiro)
class SolicitudRetiroAdmin(admin.ModelAdmin):
    list_display = ('ciudadano', 'material', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'material')
    search_fields = ('ciudadano__username',)
