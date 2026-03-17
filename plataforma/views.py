import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from .models import Perfil, ParametroGlobal, Modulo, LogAccion, Staff
from .decorators import rol_requerido, solo_administrador, registrar_accion, get_client_ip
from .services import ParametroService, ModuloService, UsuarioService, AuditoriaService
from core.models import ContenidoInicio, Noticia
from .forms import StaffForm
import cloudinary
import cloudinary.uploader
import os
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def extract_youtube_id(url):
    regex = r"(?:v=|youtu\.be\/|embed\/)([A-Za-z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

# Función para subir archivos a Cloudinary de forma unsigned
def upload_unsigned(file, preset, folder):
    # Subida unsigned normal, sin tocar api_secret
    result = cloudinary.uploader.upload(
        file,
        upload_preset=preset,
        folder=folder,
        unsigned=True  # importante para preset unsigned
    )
    return result

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
        return redirect('plataforma_login')
    
    rol = request.user.perfil.rol
    if rol == 'ADMINISTRADOR':
        return redirect('dashboard_admin')
    elif rol == 'PADRE':
        return redirect('dashboard_padre')
    else:
        messages.error(request, 'Rol no reconocido.')
        return redirect('plataforma_login')

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
    estudiantes = padre.estudiantes.all() if padre else []
    
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
    
    context = {'parametros': parametros, 'fecha_corte_ludicas': fecha_corte_ludicas}
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
    return render(request, 'plataforma/gestionar_modulos.html', {'modulos': modulos})

# ============================================
# GESTIÓN DE USUARIOS
# ============================================

@solo_administrador
def gestionar_usuarios(request):
    usuarios = User.objects.select_related('perfil').all()
    stats = UsuarioService.obtener_estadisticas()
    return render(request, 'plataforma/gestionar_usuarios.html', {'usuarios': usuarios, 'stats': stats})

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
            if user == request.user:
                messages.error(request, 'No puedes eliminar tu propia cuenta')
                return redirect('gestionar_usuarios')
            username = user.username
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

# ============================================
# GESTIÓN DE INICIO (HERO Y NOTICIAS)
# ============================================

def gestionar_inicio(request):
    contenido, _ = ContenidoInicio.objects.get_or_create(id=1)
    preset = os.getenv("CLOUDINARY_UPLOAD_PRESET", "preset_publico")  # preset unsigned

    # ==== GUARDAR HERO ====
    if request.method == "POST" and "guardar_hero" in request.POST:
        for field in ["hero_imagen1", "hero_imagen2"]:
            file = request.FILES.get(field)
            if file:
                upload_result = upload_unsigned(file, preset=preset, folder="cedhu/hero")
                setattr(contenido, field, upload_result['secure_url'])

        # Guardar video
        video = request.POST.get("hero_video")
        video_id = extract_youtube_id(video) if video else None
        if video_id:
            contenido.hero_video = video_id

        contenido.save()
        return redirect("gestionar_inicio")

    # ==== CREAR NOTICIA ====
    if request.method == "POST" and "crear_noticia" in request.POST:
        imagen = request.FILES.get("imagen_noticia")
        url = request.POST.get("url_noticia", "").strip()
        if imagen:
            upload_result = upload_unsigned(imagen, preset=preset, folder="cedhu/noticias")

            # Validar URL antes de guardar
            if url:
                validate = URLValidator()
                try:
                    validate(url)
                except ValidationError:
                    url = None

            Noticia.objects.create(
                imagen=upload_result['secure_url'],
                url=url
            )
        return redirect("gestionar_inicio")

    noticias = Noticia.objects.filter(activa=True)
    return render(request, "plataforma/gestionar_inicio.html", {
        "contenido": contenido,
        "noticias": noticias
    })

# ============================================
# ELIMINAR NOTICIA
# ============================================

def eliminar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    noticia.delete()
    return redirect("gestionar_inicio")

# ============================================
# GESTIÓN DE NOSOTROS
# ============================================

def gestionar_nosotros(request):
    staff = Staff.objects.all().order_by('categoria', 'nombre')
    form = StaffForm()
    preset = os.getenv("CLOUDINARY_UPLOAD_PRESET", "preset_publico")
    folder = "cedhu/staff"

    if request.method == "POST":
        if 'crear_staff' in request.POST:
            form = StaffForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                if request.FILES.get('imagen'):
                    result = upload_unsigned(request.FILES['imagen'], preset=preset, folder=folder)
                    instance.imagen = result['secure_url']
                instance.save()
                return redirect('gestionar_nosotros')

        elif 'editar_staff' in request.POST:
            staff_id = request.POST.get('staff_id')
            persona = get_object_or_404(Staff, id=staff_id)
            form = StaffForm(request.POST, request.FILES, instance=persona)
            if form.is_valid():
                instance = form.save(commit=False)
                if request.FILES.get('imagen'):
                    result = upload_unsigned(request.FILES['imagen'], preset=preset, folder=folder)
                    instance.imagen = result['secure_url']
                instance.save()
                return redirect('gestionar_nosotros')

        elif 'eliminar_staff' in request.POST:
            staff_id = request.POST.get('staff_id')
            persona = get_object_or_404(Staff, id=staff_id)
            persona.delete()
            return redirect('gestionar_nosotros')

    return render(request, 'plataforma/gestionar_nosotros.html', {
        'staff': staff,
        'form': form
    })

def nosotros_publico(request):
    directivas = Staff.objects.filter(categoria='directivas').order_by('nombre')
    coordinadores = Staff.objects.filter(categoria='coordinadores').order_by('nombre')
    docentes = Staff.objects.filter(categoria='docentes').order_by('nombre')
    administrativos = Staff.objects.filter(categoria='administrativos').order_by('nombre')
    servicios = Staff.objects.filter(categoria='servicios').order_by('nombre')

    return render(request, 'plataforma/nosotros.html', {
        'directivas': directivas,
        'coordinadores': coordinadores,
        'docentes': docentes,
        'administrativos': administrativos,
        'servicios': servicios
    })