from django.contrib import admin
from .models import Padre


class EstudianteInline(admin.TabularInline):
    """Muestra los estudiantes dentro del formulario de Padre"""
    from estudiantes.models import Estudiante
    model = Estudiante
    extra = 1  # Permite agregar 1 estudiante nuevo directamente
    fields = ['nombres', 'apellidos', 'documento', 'fecha_nacimiento', 'grado']
    can_delete = True


@admin.register(Padre)
class PadreAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'correo', 'documento', 'telefono', 'numero_estudiantes', 'fecha_creacion']
    search_fields = ['nombres', 'apellidos', 'correo', 'documento']
    list_filter = ['fecha_creacion']
    inlines = [EstudianteInline]  # ✅ Muestra estudiantes relacionados
    
    def numero_estudiantes(self, obj):
        """Muestra cuántos estudiantes tiene el padre"""
        count = obj.estudiantes.count()
        return f"{count} estudiante{'s' if count != 1 else ''}"
    
    numero_estudiantes.short_description = 'Estudiantes'
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'correo', 'documento')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'direccion')
        }),
    )