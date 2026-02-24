from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Crea automáticamente un Perfil cuando se crea un User.
    Si es superusuario o staff → rol ADMINISTRADOR (sin validación de Padre).
    Si es usuario normal → rol PADRE.
    """
    if created:
        if not hasattr(instance, 'perfil'):
            rol = 'ADMINISTRADOR' if (instance.is_superuser or instance.is_staff) else 'PADRE'
            Perfil.objects.create(user=instance, rol=rol)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()