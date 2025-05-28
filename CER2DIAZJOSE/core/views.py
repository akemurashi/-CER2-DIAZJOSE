from django.shortcuts import render, redirect
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from django.utils.timezone import now
from datetime import datetime
from .models import SolicitudRetiro
import calendar
from django.db import models
from .models import MATERIALES
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def materiales(request):
    return render(request, 'core/materiales.html')

def puntos_limpios(request):
    return render(request, 'core/puntos_limpios.html')

def recomendaciones(request):
    return render(request, 'core/recomendaciones.html')

def metricas(request):
    solicitudes = SolicitudRetiro.objects.all()

    # Solicitudes por mes
    por_mes = (
        solicitudes
        .annotate(mes=models.functions.ExtractMonth('fecha_creacion'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    datos_mes = [
        {'mes': calendar.month_name[d['mes']], 'total': d['total']} for d in por_mes
    ]

    # Material más solicitado
    material_popular = (
        solicitudes
        .values('material')
        .annotate(total=Count('id'))
        .order_by('-total')
        .first()
    )
    material_mas_reciclado = dict(MATERIALES).get(material_popular['material'], 'N/A') if material_popular else 'N/A'

    # Promedio de días entre creación y completado
    completadas = solicitudes.filter(estado='COM', fecha_completada__isnull=False).annotate(
        tiempo=ExpressionWrapper(
            F('fecha_completada') - F('fecha_creacion'),
            output_field=DurationField()
        )
    )
    promedio_dias = completadas.aggregate(promedio=Avg('tiempo'))['promedio']
    promedio_dias = round(promedio_dias.total_seconds() / 86400, 1) if promedio_dias else 'N/A'

    return render(request, 'core/metricas.html', {
        'solicitudes_mes': datos_mes,
        'material_mas_reciclado': material_mas_reciclado,
        'promedio_dias': promedio_dias,
    })

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo = Group.objects.get(name='Ciudadano')
            user.groups.add(grupo)
            return redirect('login')  # necesitarás una vista de login más adelante
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

@login_required
def nueva_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.ciudadano = request.user
            solicitud.save()
            return redirect('historial_solicitudes')  # lo crearemos en el paso 8
    else:
        form = SolicitudForm()
    return render(request, 'core/nueva_solicitud.html', {'form': form})