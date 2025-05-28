from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from core.models import SolicitudRetiro
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = "Inicializa los grupos de usuarios: Ciudadano, Operario y Staff"

    def handle(self, *args, **kwargs):
        # Crear grupo Operario
        operario_group, _ = Group.objects.get_or_create(name='Operario')
        perms = Permission.objects.filter(content_type=ContentType.objects.get_for_model(SolicitudRetiro))
        operario_group.permissions.set(perms)

        # Grupo Ciudadano (sin permisos especiales)
        Group.objects.get_or_create(name='Ciudadano')

        self.stdout.write(self.style.SUCCESS('Grupos creados con éxito.'))
