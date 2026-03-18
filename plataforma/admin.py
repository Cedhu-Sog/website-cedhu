from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfil, ParametroGlobal, Modulo, LogAccion, Staff
from .forms import StaffForm


# ============================================
# INLINE ADMIN: Perfil dentro de User
# ============================================
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'
    extra = 0


# ============================================
# EXTENDER UserAdmin para incluir Perfil
# ============================================
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_rol', 'get_activo', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'perfil__rol', 'perfil__activo')
    
    def get_rol(self, obj):
        if hasattr(obj, 'perfil'):
            return obj.perfil.get_rol_display()
        return '-'
    get_rol.short_description = 'Rol'
    
    def get_activo(self, obj):
        if hasattr(obj, 'perfil'):
            return '✓' if obj.perfil.activo else '✗'
        return '-'
    get_activo.short_description = 'Activo'


# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ============================================
# ADMIN: Perfil
# ============================================
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'activo', 'padre', 'fecha_creacion')
    list_filter = ('rol', 'activo', 'fecha_creacion')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'rol', 'activo')
        }),
        ('Vinculación', {
            'fields': ('padre',),
            'description': 'Solo para usuarios con rol PADRE'
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


# ============================================
# ADMIN: ParametroGlobal
# ============================================
@admin.register(ParametroGlobal)
class ParametroGlobalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor', 'fecha_modificacion')
    search_fields = ('nombre', 'valor', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    
    fieldsets = (
        ('Información del Parámetro', {
            'fields': ('nombre', 'valor', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


# ============================================
# ADMIN: Modulo
# ============================================
@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'app_label', 'activo', 'orden', 'get_roles')
    list_filter = ('activo',)
    search_fields = ('nombre', 'app_label', 'descripcion')
    ordering = ('orden', 'nombre')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'app_label', 'descripcion', 'activo')
        }),
        ('Configuración de Acceso', {
            'fields': ('roles_permitidos', 'url_base', 'icono')
        }),
        ('Visualización', {
            'fields': ('orden',)
        }),
    )
    
    def get_roles(self, obj):
        return obj.roles_permitidos
    get_roles.short_description = 'Roles Permitidos'


# ============================================
# ADMIN: LogAccion
# ============================================
@admin.register(LogAccion)
class LogAccionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'tipo_accion', 'accion_corta', 'modulo', 'ip_address')
    list_filter = ('tipo_accion', 'modulo', 'fecha')
    search_fields = ('usuario__username', 'accion', 'detalles')
    readonly_fields = ('usuario', 'tipo_accion', 'accion', 'modulo', 'detalles', 'ip_address', 'fecha')
    date_hierarchy = 'fecha'
    
    def accion_corta(self, obj):
        return obj.accion[:50] + '...' if len(obj.accion) > 50 else obj.accion
    accion_corta.short_description = 'Acción'
    
    def has_add_permission(self, request):
        """No permitir agregar logs manualmente desde el admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """No permitir editar logs"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Solo superusuarios pueden eliminar logs"""
        return request.user.is_superuser


# ============================================
# PERSONALIZACIÓN DEL ADMIN
# ============================================
admin.site.site_header = "Administración CEDHU"
admin.site.site_title = "CEDHU Admin"
admin.site.index_title = "Panel de Administración"

# ============================================
# ADMIN: Staff
# ============================================
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffForm
    list_display = ('nombre', 'cargo', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'cargo', 'descripcion')
