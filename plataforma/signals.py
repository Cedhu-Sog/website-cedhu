from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Signal que crea automáticamente un Perfil cuando se crea un User.
    Por defecto, el rol será PADRE.
    """
    if created:
        # Solo crear perfil si no existe
        if not hasattr(instance, 'perfil'):
            Perfil.objects.create(user=instance, rol='PADRE')


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """
    Signal que guarda el perfil cuando se guarda el usuario.
    """
    if hasattr(instance, 'perfil'):
        instance.perfil.save()