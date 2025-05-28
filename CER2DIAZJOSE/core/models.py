from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

MATERIALES = [
    ('PAP', 'Papel y cartón'),
    ('PLAS', 'Plásticos reciclables'),
    ('VID', 'Vidrios'),
    ('LAT', 'Latas'),
    ('ELEC', 'Electrónicos pequeños'),
    ('TEX', 'Textiles'),
    ('VOL', 'Voluminosos reciclables'),
]

ESTADOS = [
    ('PEN', 'Pendiente'),
    ('RUT', 'En ruta'),
    ('COM', 'Completada'),
]

class SolicitudRetiro(models.Model):
    ciudadano = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.CharField(max_length=10, choices=MATERIALES)
    cantidad = models.PositiveIntegerField()
    fecha_estimada = models.DateField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_completada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN')
    comentario_operario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ciudadano.username} - {self.get_material_display()} - {self.estado}"

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - Perfil"

# Crear perfil automáticamente al crear usuario
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)