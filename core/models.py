from django.db import models
from cloudinary.models import CloudinaryField


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


class Noticia(models.Model):
    titulo = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Título",
        help_text="Título opcional de la noticia."
    )
    imagen = CloudinaryField(
        'imagen',
        folder='noticias/',
        blank=True,
        null=True,
        transformation={'quality': 'auto', 'fetch_format': 'auto'}
    )
    url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Link (opcional)",
        help_text="Si añades un link, al hacer clic en la imagen se abrirá esa URL. Si lo dejas vacío, la imagen se ampliará."
    )
    fecha = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"

    def __str__(self):
        if self.titulo:
            return self.titulo
        return f"Noticia #{self.id} — {self.fecha.strftime('%d/%m/%Y')}"