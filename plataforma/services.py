"""
Servicios y lógica de negocio de la plataforma.
Separar la lógica de negocio de las vistas para mejor mantenibilidad.
"""

from .models import ParametroGlobal, Modulo, LogAccion
from django.contrib.auth.models import User
from datetime import datetime


class ParametroService:
    """Servicio para gestión de parámetros globales"""
    
    @staticmethod
    def obtener_fecha_corte_ludicas():
        """Obtiene la fecha de corte para lúdicas"""
        valor = ParametroGlobal.obtener('fecha_corte_ludicas')
        if valor:
            try:
                return datetime.strptime(valor, '%Y-%m-%d').date()
            except ValueError:
                return None
        return None
    
    @staticmethod
    def establecer_fecha_corte_ludicas(fecha):
        """Establece la fecha de corte para lúdicas"""
        if isinstance(fecha, str):
            fecha_str = fecha
        else:
            fecha_str = fecha.strftime('%Y-%m-%d')
        
        parametro, created = ParametroGlobal.objects.update_or_create(
            nombre='fecha_corte_ludicas',
            defaults={
                'valor': fecha_str,
                'descripcion': 'Fecha límite para inscripción en actividades lúdicas'
            }
        )
        return parametro
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los parámetros globales"""
        return ParametroGlobal.objects.all()
    
    @staticmethod
    def actualizar_parametro(nombre, valor, descripcion=''):
        """Actualiza o crea un parámetro"""
        parametro, created = ParametroGlobal.objects.update_or_create(
            nombre=nombre,
            defaults={
                'valor': valor,
                'descripcion': descripcion
            }
        )
        return parametro, created


class ModuloService:
    """Servicio para gestión de módulos"""
    
    @staticmethod
    def obtener_modulos_activos():
        """Obtiene todos los módulos activos"""
        return Modulo.objects.filter(activo=True).order_by('orden')
    
    @staticmethod
    def obtener_modulos_por_rol(rol):
        """Obtiene módulos disponibles para un rol específico"""
        modulos = Modulo.objects.filter(activo=True).order_by('orden')
        return [m for m in modulos if m.puede_acceder(rol)]
    
    @staticmethod
    def activar_modulo(app_label):
        """Activa un módulo"""
        try:
            modulo = Modulo.objects.get(app_label=app_label)
            modulo.activo = True
            modulo.save()
            return True, f"Módulo {modulo.nombre} activado"
        except Modulo.DoesNotExist:
            return False, "Módulo no encontrado"
    
    @staticmethod
    def desactivar_modulo(app_label):
        """Desactiva un módulo"""
        try:
            modulo = Modulo.objects.get(app_label=app_label)
            modulo.activo = False
            modulo.save()
            return True, f"Módulo {modulo.nombre} desactivado"
        except Modulo.DoesNotExist:
            return False, "Módulo no encontrado"


class UsuarioService:
    """Servicio para gestión de usuarios y perfiles"""
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de usuarios"""
        from .models import Perfil
        
        total_usuarios = User.objects.count()
        administradores = Perfil.objects.filter(rol='ADMINISTRADOR').count()
        padres = Perfil.objects.filter(rol='PADRE').count()
        activos = Perfil.objects.filter(activo=True).count()
        inactivos = Perfil.objects.filter(activo=False).count()
        
        return {
            'total': total_usuarios,
            'administradores': administradores,
            'padres': padres,
            'activos': activos,
            'inactivos': inactivos
        }
    
    @staticmethod
    def crear_usuario_padre(username, email, password, padre_obj):
        """Crea un usuario con rol PADRE vinculado a un Padre"""
        from .models import Perfil
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Actualizar perfil (creado automáticamente por signal)
        perfil = user.perfil
        perfil.rol = 'PADRE'
        perfil.padre = padre_obj
        perfil.save()
        
        return user
    
    @staticmethod
    def crear_usuario_administrador(username, email, password, first_name='', last_name=''):
        """Crea un usuario con rol ADMINISTRADOR"""
        from .models import Perfil
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Actualizar perfil
        perfil = user.perfil
        perfil.rol = 'ADMINISTRADOR'
        perfil.save()
        
        return user
    
    @staticmethod
    def activar_usuario(user_id):
        """Activa un usuario"""
        try:
            user = User.objects.get(id=user_id)
            user.perfil.activo = True
            user.perfil.save()
            return True, f"Usuario {user.username} activado"
        except User.DoesNotExist:
            return False, "Usuario no encontrado"
    
    @staticmethod
    def desactivar_usuario(user_id):
        """Desactiva un usuario"""
        try:
            user = User.objects.get(id=user_id)
            user.perfil.activo = False
            user.perfil.save()
            return True, f"Usuario {user.username} desactivado"
        except User.DoesNotExist:
            return False, "Usuario no encontrado"


class AuditoriaService:
    """Servicio para consultas de auditoría"""
    
    @staticmethod
    def obtener_logs_recientes(limite=50):
        """Obtiene los logs más recientes"""
        return LogAccion.objects.all()[:limite]
    
    @staticmethod
    def obtener_logs_usuario(user, limite=50):
        """Obtiene los logs de un usuario específico"""
        return LogAccion.objects.filter(usuario=user)[:limite]
    
    @staticmethod
    def obtener_logs_por_tipo(tipo_accion, limite=50):
        """Obtiene logs de un tipo específico"""
        return LogAccion.objects.filter(tipo_accion=tipo_accion)[:limite]
    
    @staticmethod
    def obtener_logs_por_modulo(modulo, limite=50):
        """Obtiene logs de un módulo específico"""
        return LogAccion.objects.filter(modulo=modulo)[:limite]
    
    @staticmethod
    def estadisticas_actividad():
        """Genera estadísticas de actividad"""
        from django.db.models import Count
        
        por_tipo = LogAccion.objects.values('tipo_accion').annotate(
            total=Count('id')
        ).order_by('-total')
        
        por_usuario = LogAccion.objects.values('usuario__username').annotate(
            total=Count('id')
        ).order_by('-total')[:10]
        
        return {
            'por_tipo': list(por_tipo),
            'por_usuario': list(por_usuario)
        }