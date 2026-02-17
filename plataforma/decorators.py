from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import LogAccion


def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def rol_requerido(*roles_permitidos):
    """
    Decorador que verifica si el usuario tiene uno de los roles especificados.
    
    Uso:
        @rol_requerido('ADMINISTRADOR')
        def mi_vista(request):
            ...
        
        @rol_requerido('ADMINISTRADOR', 'PADRE')
        def otra_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificar que el usuario esté autenticado
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder.')
                return redirect('login')
            
            # Verificar que el usuario tenga perfil
            if not hasattr(request.user, 'perfil'):
                messages.error(request, 'Tu cuenta no tiene un perfil asignado. Contacta al administrador.')
                return redirect('login')
            
            # Verificar que el perfil esté activo
            if not request.user.perfil.activo:
                messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
                return redirect('login')
            
            # Verificar el rol
            rol_usuario = request.user.perfil.rol
            if rol_usuario not in roles_permitidos:
                messages.error(request, 'No tienes permisos para acceder a esta sección.')
                
                # Registrar intento de acceso no autorizado
                LogAccion.registrar(
                    usuario=request.user,
                    accion=f'Intento de acceso no autorizado a: {request.path}',
                    tipo_accion='OTRO',
                    modulo='plataforma',
                    detalles=f'Rol requerido: {roles_permitidos}, Rol del usuario: {rol_usuario}',
                    ip=get_client_ip(request)
                )
                
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def solo_administrador(view_func):
    """
    Decorador que permite acceso solo a administradores.
    Es un atajo para @rol_requerido('ADMINISTRADOR')
    """
    return rol_requerido('ADMINISTRADOR')(view_func)


def solo_padre(view_func):
    """
    Decorador que permite acceso solo a padres.
    Es un atajo para @rol_requerido('PADRE')
    """
    return rol_requerido('PADRE')(view_func)


def registrar_accion(tipo_accion, descripcion_base, modulo=''):
    """
    Decorador que registra automáticamente una acción en el log.
    
    Uso:
        @registrar_accion('VER', 'Visualizó el dashboard', modulo='plataforma')
        def dashboard_admin(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Ejecutar la vista
            response = view_func(request, *args, **kwargs)
            
            # Registrar la acción
            if request.user.is_authenticated:
                LogAccion.registrar(
                    usuario=request.user,
                    accion=descripcion_base,
                    tipo_accion=tipo_accion,
                    modulo=modulo,
                    ip=get_client_ip(request)
                )
            
            return response
        return wrapper
    return decorator