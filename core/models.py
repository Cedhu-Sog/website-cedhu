from django.db import models

class ContenidoInicio(models.Model):
    titulo_galeria = models.CharField(max_length=255, blank=True)
    url_manual = models.URLField(blank=True)
    texto_direccion = models.TextField(blank=True)
    iframe_mapa = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    imagen_manual = models.ImageField(upload_to='manuales/', blank=True, null=True)

class GalleryImage(models.Model):
    contenido = models.ForeignKey(
        ContenidoInicio,
        related_name='gallery_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='gallery/')
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField()

    class Meta:
        unique_together = ('contenido', 'orden')

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    portada = models.ImageField(upload_to='eventos/')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Eventos"
        ordering = ['fecha', 'hora']
