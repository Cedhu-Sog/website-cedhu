from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


# ============================================
# GRADOS disponibles (igual que en Estudiante)
# ============================================
GRADOS_CHOICES = [
    ('PRIMERO',    'Primero'),
    ('SEGUNDO',    'Segundo'),
    ('TERCERO',    'Tercero'),
    ('CUARTO',     'Cuarto'),
    ('QUINTO',     'Quinto'),
    ('SEXTO',      'Sexto'),
    ('SEPTIMO',    'Séptimo'),
    ('OCTAVO',     'Octavo'),
    ('NOVENO',     'Noveno'),
    ('DECIMO',     'Décimo'),
    ('ONCE',       'Once'),
]


# ============================================
# MODELO: ProfesorLudica
# ============================================
class ProfesorLudica(models.Model):
    """
    Docente encargado de una o varias lúdicas.
    Creado y gestionado por el administrador.
    """
    nombres      = models.CharField(max_length=100)
    apellidos    = models.CharField(max_length=100)
    documento    = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r'^[0-9]+$', 'Solo números.')],
        help_text="Número de documento (solo dígitos)"
    )
    correo       = models.EmailField(unique=True)
    telefono     = models.CharField(max_length=15, blank=True)
    especialidad = models.CharField(
        max_length=150,
        blank=True,
        help_text="Área o especialidad del docente (ej: Arte, Deportes, Música)"
    )
    activo       = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Vinculo opcional con User de Django (para acceso futuro)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='profesor_ludica',
        help_text="Cuenta de acceso al sistema (opcional)"
    )

    class Meta:
        verbose_name = "Profesor de Lúdica"
        verbose_name_plural = "Profesores de Lúdicas"
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"


# ============================================
# MODELO: Ludica
# ============================================
class Ludica(models.Model):
    """
    Actividad lúdica ofrecida por la institución.
    El administrador la crea y asigna profesor y grados.
    """
    ESTADOS = [
        ('ACTIVA',    'Activa'),
        ('INACTIVA',  'Inactiva'),
        ('COMPLETA',  'Cupo completo'),
    ]

    nombre      = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    profesor    = models.ForeignKey(
        ProfesorLudica,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='ludicas',
        help_text="Docente responsable"
    )

    # Grados que PUEDEN inscribirse (lista separada por comas internamente)
    grados_permitidos = models.JSONField(
        default=list,
        help_text="Lista de grados que pueden inscribirse en esta lúdica"
    )

    cupo_maximo = models.PositiveIntegerField(
        default=30,
        help_text="Número máximo de estudiantes"
    )

    horario = models.CharField(
        max_length=200,
        blank=True,
        help_text="Ej: Lunes y Miércoles 2:00 - 4:00 PM"
    )

    lugar = models.CharField(
        max_length=150,
        blank=True,
        help_text="Aula, cancha, sala, etc."
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='ACTIVA'
    )

    icono = models.CharField(
        max_length=50,
        blank=True,
        default='fa-star',
        help_text="Clase de icono Font Awesome (ej: fa-music, fa-futbol)"
    )

    color = models.CharField(
        max_length=7,
        blank=True,
        default='#4f46e5',
        help_text="Color hex de la tarjeta (ej: #4f46e5)"
    )

    fecha_creacion   = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lúdica"
        verbose_name_plural = "Lúdicas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def cupos_disponibles(self):
        inscritos = self.inscripciones.filter(activa=True).count()
        return max(0, self.cupo_maximo - inscritos)

    @property
    def total_inscritos(self):
        return self.inscripciones.filter(activa=True).count()

    @property
    def esta_llena(self):
        return self.cupos_disponibles == 0

    def grados_display(self):
        """Retorna los grados como texto legible"""
        mapa = dict(GRADOS_CHOICES)
        return [mapa.get(g, g) for g in self.grados_permitidos]


# ============================================
# MODELO: EstudianteLudica (perfil de estudiante en lúdicas)
# ============================================
class EstudianteLudica(models.Model):
    """
    Perfil de estudiante dentro del sistema de lúdicas.
    Creado por el administrador. Tiene su propio acceso.
    """
    estudiante = models.OneToOneField(
        'estudiantes.Estudiante',
        on_delete=models.CASCADE,
        related_name='perfil_ludica',
        help_text="Estudiante del sistema principal"
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='estudiante_ludica',
        help_text="Cuenta de acceso para el estudiante"
    )

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Estudiante en Lúdicas"
        verbose_name_plural = "Estudiantes en Lúdicas"
        ordering = ['estudiante__apellidos']

    def __str__(self):
        return f"{self.estudiante.nombres} {self.estudiante.apellidos}"

    @property
    def nombre_completo(self):
        return f"{self.estudiante.nombres} {self.estudiante.apellidos}"

    @property
    def grado(self):
        return self.estudiante.grado

    @property
    def inscripcion_activa(self):
        """Retorna la inscripción activa del estudiante (solo puede tener 1)"""
        return self.inscripciones.filter(activa=True).first()

    @property
    def tiene_ludica(self):
        return self.inscripciones.filter(activa=True).exists()


# ============================================
# MODELO: Inscripcion
# ============================================
class Inscripcion(models.Model):
    """
    Registro de un estudiante inscrito en una lúdica.
    Cada estudiante puede estar en máximo UNA lúdica activa.
    """
    estudiante = models.ForeignKey(
        EstudianteLudica,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    ludica = models.ForeignKey(
        Ludica,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    notas_admin = models.TextField(blank=True, help_text="Notas internas del administrador")

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        ordering = ['-fecha_inscripcion']
        # Un estudiante no puede estar dos veces en la misma lúdica activa
        unique_together = ('estudiante', 'ludica')

    def __str__(self):
        return f"{self.estudiante} → {self.ludica}"

    def save(self, *args, **kwargs):
        """
        Valida que:
        1. El estudiante no tenga otra inscripción activa.
        2. La lúdica tenga cupo disponible.
        3. El grado del estudiante esté permitido.
        """
        if self.activa and not self.pk:
            # Verificar inscripción activa previa
            if self.estudiante.inscripciones.filter(activa=True).exists():
                raise ValueError("El estudiante ya está inscrito en una lúdica.")

            # Verificar cupo
            if self.ludica.esta_llena:
                raise ValueError("La lúdica no tiene cupos disponibles.")

            # Verificar grado permitido
            grado_est = self.estudiante.grado
            if self.ludica.grados_permitidos and grado_est not in self.ludica.grados_permitidos:
                raise ValueError(
                    f"El grado '{grado_est}' no está permitido en esta lúdica."
                )

        super().save(*args, **kwargs)

        # Actualizar estado de la lúdica si se llenó
        ludica = self.ludica
        if ludica.esta_llena and ludica.estado == 'ACTIVA':
            ludica.estado = 'COMPLETA'
            ludica.save(update_fields=['estado'])