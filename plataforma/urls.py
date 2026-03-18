from django.shortcuts import redirect
from django.urls import path

from plataforma.models import Noticia
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='plataforma_login'),
    path('logout/', views.logout_view, name='plataforma_logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    
    # Dashboards
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/padre/', views.dashboard_padre, name='dashboard_padre'),
    
    # Gestión de Parámetros
    path('parametros/', views.gestionar_parametros, name='gestionar_parametros'),
    path('parametros/eliminar/<int:parametro_id>/', views.eliminar_parametro, name='eliminar_parametro'),
    
    # Gestión de Módulos
    path('modulos/', views.gestionar_modulos, name='gestionar_modulos'),
    
    # Gestión de Usuarios
    path('usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('usuarios/toggle/<int:user_id>/', views.toggle_usuario, name='toggle_usuario'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # Auditoría
    path('auditoria/', views.ver_auditoria, name='ver_auditoria'),
    path('gestionar-inicio/', views.gestionar_inicio, name='gestionar_inicio'),
    path('noticias/eliminar/<int:noticia_id>/',views.eliminar_noticia,name='eliminar_noticia'),
    path('nosotros/', views.gestionar_nosotros, name='gestionar_nosotros'),
    path('nosotros-publico/', views.nosotros_publico, name='nosotros_publico'), 
]