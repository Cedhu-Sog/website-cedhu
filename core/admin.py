from django.contrib import admin
from .models import Noticia, ContenidoInicio, GalleryImage, Evento


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'activa', 'url')
    list_editable = ('activa',)
    list_filter = ('activa',)
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)


@admin.register(ContenidoInicio)
class ContenidoInicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo_galeria')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'contenido', 'orden', 'descripcion')
    ordering = ('contenido', 'orden')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'fecha', 'hora')
    ordering = ('fecha', 'hora')