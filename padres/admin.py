from django.contrib import admin
from .models import Padre

@admin.register(Padre)
class PadreAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'correo', 'documento', 'telefono')
    search_fields = ('nombres', 'apellidos', 'correo', 'documento')
    list_filter = ('fecha_creacion',)
