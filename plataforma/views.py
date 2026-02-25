from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from datetime import datetime

from .models import Perfil, ParametroGlobal, Modulo, LogAccion
from .decorators import rol_requerido, solo_administrador, registrar_accion, get_client_ip
from .services import (
    ParametroService, ModuloService, 
    UsuarioService, AuditoriaService
)


# ============================================
# AUTENTICACIÓN
# ============================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not hasattr(user, 'perfil'):
                messages.error(request, 'Tu cuenta no tiene un perfil asignado. Contacta al administrador.')
                return render(request, 'plataforma/login.html')
            
            if not user.perfil.activo:
                messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
                return render(request, 'plataforma/login.html')
            
            login(request, user)
            
            LogAccion.registrar(
                usuario=user,
                accion='Inicio de sesión exitoso',
                tipo_accion='LOGIN',
                modulo='plataforma',
                ip=get_client_ip(request)
            )
            
            messages.success(request, f'Bienvenido, {user.first_name or user.username}')
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            
            LogAccion.objects.create(
                usuario=None,
                accion=f'Intento de login fallido: {username}',
                tipo_accion='LOGIN',
                modulo='plataforma',
                detalles=f'Username: {username}',
                ip_address=get_client_ip(request)
            )
    
    return render(request, 'plataforma/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        LogAccion.registrar(
            usuario=request.user,
            accion='Cierre de sesión',
            tipo_accion='LOGOUT',
            modulo='plataforma',
            ip=get_client_ip(request)
        )
    
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('home')


@login_required
def dashboard_redirect(request):
    if not hasattr(request.user, 'perfil'):
        messages.error(request, 'Tu cuenta no tiene un perfil asignado.')
        return redirect('plataforma_login')  # ← CAMBIADO
    
    rol = request.user.perfil.rol
    
    if rol == 'ADMINISTRADOR':
        return redirect('dashboard_admin')
    elif rol == 'PADRE':
        return redirect('dashboard_padre')
    else:
        messages.error(request, 'Rol no reconocido.')
        return redirect('plataforma_login')  # ← CAMBIADO


# ============================================
# DASHBOARDS
# ============================================

@rol_requerido('ADMINISTRADOR')
@registrar_accion('VER', 'Accedió al dashboard de administrador', modulo='plataforma')
def dashboard_admin(request):
    stats_usuarios = UsuarioService.obtener_estadisticas()
    modulos_activos = ModuloService.obtener_modulos_activos()
    parametros = ParametroService.obtener_todos()
    logs_recientes = AuditoriaService.obtener_logs_recientes(limite=10)
    fecha_corte_ludicas = ParametroService.obtener_fecha_corte_ludicas()
    
    context = {
        'stats_usuarios': stats_usuarios,
        'modulos_activos': modulos_activos,
        'parametros': parametros,
        'logs_recientes': logs_recientes,
        'fecha_corte_ludicas': fecha_corte_ludicas,
    }
    
    return render(request, 'plataforma/dashboard_admin.html', context)


@rol_requerido('PADRE')
@registrar_accion('VER', 'Accedió al dashboard de padre', modulo='plataforma')
def dashboard_padre(request):
    modulos_disponibles = ModuloService.obtener_modulos_por_rol('PADRE')
    perfil = request.user.perfil
    padre = perfil.padre
    estudiantes = []
    if padre:
        estudiantes = padre.estudiantes.all()
    
    context = {
        'modulos_disponibles': modulos_disponibles,
        'padre': padre,
        'estudiantes': estudiantes,
    }
    
    return render(request, 'plataforma/dashboard_padre.html', context)


# ============================================
# GESTIÓN DE PARÁMETROS GLOBALES
# ============================================

@solo_administrador
def gestionar_parametros(request):
    if request.method == 'POST':
        if 'fecha_corte_ludicas' in request.POST:
            fecha = request.POST.get('fecha_corte_ludicas')
            try:
                ParametroService.establecer_fecha_corte_ludicas(fecha)
                LogAccion.registrar(
                    usuario=request.user,
                    accion=f'Actualizó fecha de corte de lúdicas a: {fecha}',
                    tipo_accion='EDITAR',
                    modulo='plataforma',
                    ip=get_client_ip(request)
                )
                messages.success(request, 'Fecha de corte actualizada correctamente')
            except Exception as e:
                messages.error(request, f'Error al actualizar fecha: {str(e)}')
        
        elif 'nombre_parametro' in request.POST:
            nombre = request.POST.get('nombre_parametro')
            valor = request.POST.get('valor_parametro')
            descripcion = request.POST.get('descripcion_parametro', '')
            try:
                parametro, created = ParametroService.actualizar_parametro(nombre, valor, descripcion)
                accion = 'Creó' if created else 'Actualizó'
                LogAccion.registrar(
                    usuario=request.user,
                    accion=f'{accion} parámetro: {nombre}',
                    tipo_accion='CREAR' if created else 'EDITAR',
                    modulo='plataforma',
                    detalles=f'Valor: {valor}',
                    ip=get_client_ip(request)
                )
                messages.success(request, f'Parámetro {nombre} guardado correctamente')
            except Exception as e:
                messages.error(request, f'Error al guardar parámetro: {str(e)}')
        
        return redirect('gestionar_parametros')
    
    parametros = ParametroService.obtener_todos()
    fecha_corte_ludicas = ParametroService.obtener_fecha_corte_ludicas()
    
    context = {
        'parametros': parametros,
        'fecha_corte_ludicas': fecha_corte_ludicas,
    }
    
    return render(request, 'plataforma/gestionar_parametros.html', context)


@solo_administrador
def eliminar_parametro(request, parametro_id):
    if request.method == 'POST':
        try:
            parametro = get_object_or_404(ParametroGlobal, id=parametro_id)
            nombre = parametro.nombre
            parametro.delete()
            LogAccion.registrar(
                usuario=request.user,
                accion=f'Eliminó parámetro: {nombre}',
                tipo_accion='ELIMINAR',
                modulo='plataforma',
                ip=get_client_ip(request)
            )
            messages.success(request, f'Parámetro {nombre} eliminado')
        except Exception as e:
            messages.error(request, f'Error al eliminar parámetro: {str(e)}')
    
    return redirect('gestionar_parametros')


# ============================================
# GESTIÓN DE MÓDULOS
# ============================================

@solo_administrador
def gestionar_modulos(request):
    if request.method == 'POST':
        modulo_id = request.POST.get('modulo_id')
        accion = request.POST.get('accion')
        try:
            modulo = get_object_or_404(Modulo, id=modulo_id)
            if accion == 'activar':
                modulo.activo = True
                modulo.save()
                messages.success(request, f'Módulo {modulo.nombre} activado')
                LogAccion.registrar(
                    usuario=request.user,
                    accion=f'Activó módulo: {modulo.nombre}',
                    tipo_accion='EDITAR',
                    modulo='plataforma',
                    ip=get_client_ip(request)
                )
            elif accion == 'desactivar':
                modulo.activo = False
                modulo.save()
                messages.success(request, f'Módulo {modulo.nombre} desactivado')
                LogAccion.registrar(
                    usuario=request.user,
                    accion=f'Desactivó módulo: {modulo.nombre}',
                    tipo_accion='EDITAR',
                    modulo='plataforma',
                    ip=get_client_ip(request)
                )
        except Exception as e:
            messages.error(request, f'Error al gestionar módulo: {str(e)}')
        
        return redirect('gestionar_modulos')
    
    modulos = Modulo.objects.all().order_by('orden')
    context = {'modulos': modulos}
    return render(request, 'plataforma/gestionar_modulos.html', context)


# ============================================
# GESTIÓN DE USUARIOS
# ============================================

@solo_administrador
def gestionar_usuarios(request):
    usuarios = User.objects.select_related('perfil').all()
    stats = UsuarioService.obtener_estadisticas()
    context = {
        'usuarios': usuarios,
        'stats': stats,
    }
    return render(request, 'plataforma/gestionar_usuarios.html', context)


@solo_administrador
def toggle_usuario(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            perfil = user.perfil
            perfil.activo = not perfil.activo
            perfil.save()
            estado = 'activado' if perfil.activo else 'desactivado'
            LogAccion.registrar(
                usuario=request.user,
                accion=f'Usuario {user.username} {estado}',
                tipo_accion='EDITAR',
                modulo='plataforma',
                ip=get_client_ip(request)
            )
            messages.success(request, f'Usuario {user.username} {estado}')
        except Exception as e:
            messages.error(request, f'Error al cambiar estado: {str(e)}')
    
    return redirect('gestionar_usuarios')


@solo_administrador
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            username = user.username
            if user == request.user:
                messages.error(request, 'No puedes eliminar tu propia cuenta')
                return redirect('gestionar_usuarios')
            user.delete()
            LogAccion.registrar(
                usuario=request.user,
                accion=f'Eliminó usuario: {username}',
                tipo_accion='ELIMINAR',
                modulo='plataforma',
                ip=get_client_ip(request)
            )
            messages.success(request, f'Usuario {username} eliminado')
        except Exception as e:
            messages.error(request, f'Error al eliminar usuario: {str(e)}')
    
    return redirect('gestionar_usuarios')


# ============================================
# AUDITORÍA
# ============================================

@solo_administrador
def ver_auditoria(request):
    tipo_filtro = request.GET.get('tipo', '')
    usuario_filtro = request.GET.get('usuario', '')
    limite = int(request.GET.get('limite', 50))
    
    logs = LogAccion.objects.all()
    
    if tipo_filtro:
        logs = logs.filter(tipo_accion=tipo_filtro)
    if usuario_filtro:
        logs = logs.filter(usuario__username__icontains=usuario_filtro)
    
    logs = logs[:limite]
    stats = AuditoriaService.estadisticas_actividad()
    
    context = {
        'logs': logs,
        'stats': stats,
        'tipos_accion': LogAccion.TIPOS_ACCION,
        'tipo_filtro': tipo_filtro,
        'usuario_filtro': usuario_filtro,
        'limite': limite,
    }
    
    return render(request, 'plataforma/ver_auditoria.html', context)