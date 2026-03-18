from django.urls import path
from . import views

urlpatterns = [

    # ── ADMIN ─────────────────────────────────────────────────────────────
    path('admin/', views.admin_dashboard_ludicas, name='admin_dashboard_ludicas'),

    # Lúdicas CRUD
    path('admin/ludicas/', views.admin_lista_ludicas, name='admin_lista_ludicas'),
    path('admin/ludicas/crear/', views.admin_crear_ludica, name='admin_crear_ludica'),
    path('admin/ludicas/<int:ludica_id>/editar/', views.admin_editar_ludica, name='admin_editar_ludica'),
    path('admin/ludicas/<int:ludica_id>/eliminar/', views.admin_eliminar_ludica, name='admin_eliminar_ludica'),
    path('admin/ludicas/<int:ludica_id>/detalle/', views.admin_detalle_ludica, name='admin_detalle_ludica'),

    # Profesores CRUD
    path('admin/profesores/', views.admin_lista_profesores, name='admin_lista_profesores'),
    path('admin/profesores/crear/', views.admin_crear_profesor, name='admin_crear_profesor'),
    path('admin/profesores/<int:profesor_id>/editar/', views.admin_editar_profesor, name='admin_editar_profesor'),
    path('admin/profesores/<int:profesor_id>/eliminar/', views.admin_eliminar_profesor, name='admin_eliminar_profesor'),

    # Estudiantes en lúdicas
    path('admin/estudiantes/', views.admin_lista_estudiantes_ludica, name='admin_lista_estudiantes_ludica'),
    path('admin/estudiantes/registrar/', views.admin_registrar_estudiante_ludica, name='admin_registrar_estudiante_ludica'),
    path('admin/estudiantes/<int:perfil_id>/toggle/', views.admin_toggle_estudiante_ludica, name='admin_toggle_estudiante_ludica'),
    path('admin/estudiantes/<int:perfil_id>/eliminar/', views.admin_eliminar_estudiante_ludica, name='admin_eliminar_estudiante_ludica'),
    path('admin/estudiantes/<int:perfil_id>/inscribir/', views.admin_inscribir_estudiante, name='admin_inscribir_estudiante'),
    path('admin/inscripciones/<int:inscripcion_id>/cancelar/', views.admin_cancelar_inscripcion, name='admin_cancelar_inscripcion'),

    # ── ESTUDIANTE ────────────────────────────────────────────────────────
    path('mi-ludica/', views.estudiante_dashboard, name='estudiante_dashboard_ludicas'),
    path('mi-ludica/escoger/<int:ludica_id>/', views.estudiante_escoger_ludica, name='estudiante_escoger_ludica'),
    path('mi-ludica/cancelar/', views.estudiante_cancelar_inscripcion, name='estudiante_cancelar_inscripcion'),
]