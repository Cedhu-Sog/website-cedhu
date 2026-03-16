from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def estudiante_ludica_requerido(view_func):
    """Decorador: solo estudiantes con perfil de lúdica activo pueden acceder."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('plataforma_login')
        if not hasattr(request.user, 'estudiante_ludica'):
            messages.error(request, 'No tienes acceso al módulo de lúdicas.')
            return redirect('home')
        if not request.user.estudiante_ludica.activo:
            messages.error(request, 'Tu cuenta de lúdicas está desactivada.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def profesor_ludica_requerido(view_func):
    """Decorador: solo profesores de lúdica pueden acceder."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('plataforma_login')
        if not hasattr(request.user, 'profesor_ludica'):
            messages.error(request, 'No tienes acceso como profesor de lúdicas.')
            return redirect('home')
        if not request.user.profesor_ludica.activo:
            messages.error(request, 'Tu cuenta de profesor está desactivada.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_requerido(view_func):
    """Decorador: solo administradores (rol ADMINISTRADOR en Perfil)."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('plataforma_login')
        if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'ADMINISTRADOR':
            messages.error(request, 'Acceso restringido a administradores.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return wrapper