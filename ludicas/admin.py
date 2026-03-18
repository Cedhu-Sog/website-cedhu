from django.contrib import admin
from .models import Ludica, ProfesorLudica, EstudianteLudica, Inscripcion


@admin.register(ProfesorLudica)
class ProfesorLudicaAdmin(admin.ModelAdmin):
    list_display  = ('nombre_completo', 'documento', 'correo', 'especialidad', 'activo')
    list_filter   = ('activo',)
    search_fields = ('nombres', 'apellidos', 'documento', 'correo')


@admin.register(Ludica)
class LudicaAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'profesor', 'estado', 'cupo_maximo', 'total_inscritos')
    list_filter   = ('estado',)
    search_fields = ('nombre',)


@admin.register(EstudianteLudica)
class EstudianteLudicaAdmin(admin.ModelAdmin):
    list_display  = ('nombre_completo', 'grado', 'activo', 'tiene_ludica')
    list_filter   = ('activo',)
    search_fields = ('estudiante__nombres', 'estudiante__apellidos', 'estudiante__documento')


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display  = ('estudiante', 'ludica', 'activa', 'fecha_inscripcion')
    list_filter   = ('activa', 'ludica')
    search_fields = ('estudiante__estudiante__nombres', 'ludica__nombre')