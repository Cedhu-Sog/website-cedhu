from django.contrib import admin
from django import forms
from .models import ContenidoInicio, Evento, Noticia  # Solo importamos lo que realmente está en core.models
from core.utils.url_choices import get_named_urls

class NoticiaAdminForm(forms.ModelForm):
    url_name = forms.ChoiceField(
        required=False,
        choices=[],
        help_text="Selecciona una página interna del sitio"
    )

    class Meta:
        model = Noticia
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["url_name"].choices = [
            ("", "— Sin enlace —")
        ] + get_named_urls()

@admin.register(ContenidoInicio)
class ContenidoInicioAdmin(admin.ModelAdmin):
    list_display = ('titulo_galeria', 'texto_direccion', 'imagen_manual')


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    form = NoticiaAdminForm
    list_display = ("titulo", "url_name", "activa", "fecha")
    list_filter = ("activa",)
    search_fields = ("titulo",)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'hora', 'portada_display')
    list_filter = ('fecha',)
    search_fields = ('nombre', 'descripcion')

    def portada_display(self, obj):
        if obj.portada:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />',
                obj.portada.url
            )
        return "Sin imagen"

    portada_display.short_description = "Portada"

