from django.contrib import admin
from .models import Estudiante


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'documento', 'grado', 'get_padre_nombre', 'fecha_creacion']
    list_filter = ['grado', 'fecha_creacion']
    search_fields = ['nombres', 'apellidos', 'documento', 'padre__nombres', 'padre__apellidos', 'padre__correo']
    ordering = ['apellidos', 'nombres']
    
    def get_padre_nombre(self, obj):
        """Muestra el nombre del padre en la lista"""
        return f"{obj.padre.nombres} {obj.padre.apellidos}"
    
    get_padre_nombre.short_description = 'Padre/Madre'
    get_padre_nombre.admin_order_field = 'padre__apellidos'
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'documento', 'fecha_nacimiento')
        }),
        ('Información Académica', {
            'fields': ('grado',)
        }),
        ('Relación Familiar', {
            'fields': ('padre',),
            'description': 'Selecciona el padre o madre responsable del estudiante'
        }),
    )