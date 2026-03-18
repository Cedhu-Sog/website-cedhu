from django.contrib import admin
from .models import Noticia, ContenidoInicio, GalleryImage, Evento
from django.utils.html import format_html  # ← esta línea faltaba


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo_display', 'imagen_preview', 'url', 'fecha', 'activa')
    list_filter = ('activa',)
    search_fields = ('titulo',)
    list_editable = ('activa',)
    ordering = ('-fecha',)

    def titulo_display(self, obj):
        return obj.titulo if obj.titulo else f"Noticia #{obj.id}"
    titulo_display.short_description = "Título"

    def imagen_preview(self, obj):
        if obj.imagen:
            url = obj.imagen.url if hasattr(obj.imagen, 'url') else str(obj.imagen)
            return format_html('<img src="{}" style="height:60px; border-radius:6px;" />', url)
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"


@admin.register(ContenidoInicio)
class ContenidoInicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'hero_video')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'contenido', 'orden', 'descripcion')
    ordering = ('contenido', 'orden')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'fecha', 'hora')
    ordering = ('fecha', 'hora')