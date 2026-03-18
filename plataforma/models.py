from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# ============================================
# MODELO: Perfil (extiende User de Django)
# ============================================
class Perfil(models.Model):
    """
    Extiende el usuario de Django para agregar roles y permisos.
    Cada usuario debe tener un perfil asociado.
    """

    ROLES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('PADRE', 'Padre'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        help_text="Usuario de Django asociado"
    )

    rol = models.CharField(
        max_length=30,
        choices=ROLES,
        default='PADRE',
        help_text="Rol del usuario en el sistema"
    )

    # Relación opcional con el modelo Padre (si el rol es PADRE)
    padre = models.OneToOneField(
        'padres.Padre',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfil_usuario',
        help_text="Vinculación con el modelo Padre (solo si rol = PADRE)"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Define si el usuario puede acceder al sistema"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"

    def clean(self):
        """Validación: Si rol es PADRE, debe tener un Padre asociado"""
        # Los superusuarios y staff se saltan la validación
        if self.user_id and self.user.is_superuser:
            return

        if self.rol == 'PADRE' and not self.padre:
            raise ValidationError({
                'padre': 'Un perfil con rol PADRE debe estar vinculado a un registro de Padre.'
            })
        if self.rol == 'ADMINISTRADOR' and self.padre:
            raise ValidationError({
                'padre': 'Un perfil ADMINISTRADOR no debe estar vinculado a un Padre.'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# ============================================
# MODELO: ParametroGlobal
# ============================================
class ParametroGlobal(models.Model):
    """
    Parámetros de configuración global del sistema.
    Evita hardcoding de valores importantes.
    """

    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre único del parámetro (ej: fecha_corte_ludicas)"
    )

    valor = models.CharField(
        max_length=255,
        help_text="Valor del parámetro"
    )

    descripcion = models.TextField(
        blank=True,
        help_text="Descripción de qué hace este parámetro"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Parámetro Global"
        verbose_name_plural = "Parámetros Globales"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre}: {self.valor}"

    @classmethod
    def obtener(cls, nombre, default=None):
        """
        Método helper para obtener un parámetro fácilmente.
        Uso: ParametroGlobal.obtener('fecha_corte_ludicas', '2024-12-31')
        """
        try:
            parametro = cls.objects.get(nombre=nombre)
            return parametro.valor
        except cls.DoesNotExist:
            return default


# ============================================
# MODELO: Modulo
# ============================================
class Modulo(models.Model):
    """
    Representa un módulo/app del sistema que puede activarse o desactivarse.
    Permite gestión modular del proyecto.
    """

    nombre = models.CharField(
        max_length=100,
        help_text="Nombre descriptivo del módulo (ej: Lúdicas)"
    )

    app_label = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre técnico de la app Django (ej: ludicas)"
    )

    descripcion = models.TextField(
        blank=True,
        help_text="Descripción del módulo"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Define si el módulo está activo en el sistema"
    )

    icono = models.CharField(
        max_length=50,
        blank=True,
        help_text="Clase CSS del icono (ej: fa-calendar para Font Awesome)"
    )

    url_base = models.CharField(
        max_length=100,
        blank=True,
        help_text="URL base del módulo (ej: /ludicas/)"
    )

    orden = models.PositiveIntegerField(
        default=0,
        help_text="Orden de visualización en menús"
    )

    roles_permitidos = models.CharField(
        max_length=255,
        default='ADMINISTRADOR',
        help_text="Roles que pueden acceder (separados por coma: ADMINISTRADOR,PADRE)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Módulo del Sistema"
        verbose_name_plural = "Módulos del Sistema"
        ordering = ['orden', 'nombre']

    def __str__(self):
        estado = "✓" if self.activo else "✗"
        return f"{estado} {self.nombre}"

    def puede_acceder(self, rol):
        """Verifica si un rol puede acceder a este módulo"""
        roles = [r.strip() for r in self.roles_permitidos.split(',')]
        return rol in roles


# ============================================
# MODELO: LogAccion
# ============================================
class LogAccion(models.Model):
    """
    Registro de auditoría de acciones importantes en el sistema.
    """

    TIPOS_ACCION = [
        ('LOGIN', 'Inicio de sesión'),
        ('LOGOUT', 'Cierre de sesión'),
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
        ('VER', 'Visualización'),
        ('EXPORTAR', 'Exportación'),
        ('OTRO', 'Otra acción'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Usuario que realizó la acción"
    )

    tipo_accion = models.CharField(
        max_length=20,
        choices=TIPOS_ACCION,
        default='OTRO'
    )

    accion = models.CharField(
        max_length=255,
        help_text="Descripción de la acción realizada"
    )

    modulo = models.CharField(
        max_length=100,
        blank=True,
        help_text="Módulo donde se realizó la acción"
    )

    detalles = models.TextField(
        blank=True,
        help_text="Información adicional de la acción"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Dirección IP desde donde se realizó la acción"
    )

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de Acción"
        verbose_name_plural = "Logs de Acciones"
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['-fecha']),
            models.Index(fields=['usuario', '-fecha']),
        ]

    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else "Anónimo"
        return f"[{self.fecha.strftime('%Y-%m-%d %H:%M')}] {usuario_str} - {self.accion}"

    @classmethod
    def registrar(cls, usuario, accion, tipo_accion='OTRO', modulo='', detalles='', ip=None):
        """
        Método helper para registrar una acción fácilmente.
        Uso: LogAccion.registrar(request.user, 'Actualizó parámetros', tipo_accion='EDITAR')
        """
        return cls.objects.create(
            usuario=usuario,
            tipo_accion=tipo_accion,
            accion=accion,
            modulo=modulo,
            detalles=detalles,
            ip_address=ip
        )

# ============================================
# Gestionar inicio 
# ============================================    

      # HERO
class ContenidoInicio(models.Model):

    titulo_galeria = models.CharField(max_length=255, blank=True)
    url_manual = models.URLField(blank=True)
    texto_direccion = models.TextField(blank=True)
    iframe_mapa = models.TextField(blank=True)

    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    imagen_manual = models.ImageField(upload_to='manuales/', blank=True, null=True)

    
    hero_imagen1 = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_imagen2 = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_video = models.URLField(blank=True)
       
#=======================================================       
       
       # noticias 
class Noticia(models.Model):
    imagen = models.URLField(max_length=2000)
    url = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

# ============================================
# Gestionar nosotros
# ============================================    
# models.py
from django.db import models
from cloudinary.models import CloudinaryField

class Staff(models.Model):
    CATEGORIAS = [
        ('directivas', 'Directivas'),
        ('coordinadores', 'Coordinadores'),
        ('docentes', 'Docentes'),
        ('administrativos', 'Administrativos'),
        ('servicios', 'Servicios Generales'),
    ]

    nombre = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    descripcion = models.TextField()
    descripcion_back = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    imagen = CloudinaryField('imagen')

    def __str__(self):
        return self.nombre
