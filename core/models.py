from django.db import models
from cloudinary.models import CloudinaryField


class ContenidoInicio(models.Model):
    titulo_galeria = models.CharField(max_length=255, blank=True)
    url_manual = models.URLField(blank=True)
    texto_direccion = models.TextField(blank=True)
    iframe_mapa = models.TextField(blank=True)
    logo = CloudinaryField('image', folder='logos', blank=True, null=True)
    imagen_manual = CloudinaryField('image', folder='manuales', blank=True, null=True)


class GalleryImage(models.Model):
    contenido = models.ForeignKey(
        ContenidoInicio,
        related_name='gallery_images',
        on_delete=models.CASCADE
    )
    image = CloudinaryField('image', folder='gallery')
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField()

    class Meta:
        unique_together = ('contenido', 'orden')


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    portada = CloudinaryField(
        'image',
        folder='eventos',
        transformation={
            'width': 800, 'height': 1000,  # proporción 4:5
            'crop': 'fill',
            'quality': 'auto',
            'fetch_format': 'auto',
        }
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Eventos"
        ordering = ['fecha', 'hora']


class Noticia(models.Model):
    imagen = CloudinaryField(
        'image',
        folder='noticias',
        transformation={
            'height': 1000,
    'crop': 'limit',
    'quality': 'auto:good',
    'fetch_format': 'auto',
        }
    )
    url = models.URLField(
        blank=True,
        null=True,
        help_text="URL externa de la noticia. Si se deja vacío, al hacer clic se abrirá la imagen directamente."
    )
    fecha = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"

    def __str__(self):
        return f"Noticia #{self.id} — {self.fecha.strftime('%d/%m/%Y')}"