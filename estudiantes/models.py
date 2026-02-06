from django.db import models
from padres.models import Padre
from django.core.validators import RegexValidator


class Estudiante(models.Model):
    # 🔗 Relación con Padre (obligatoria)
    padre = models.ForeignKey(
        Padre,
        on_delete=models.CASCADE,
        related_name='estudiantes',
        help_text="Padre responsable del estudiante"
    )

    # 📝 Datos personales
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    # 🆔 Documento (único)
    documento = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]+$',
                message='El documento solo debe contener números.'
            )
        ],
        help_text="Documento de identidad del estudiante"
    )

    # 🎂 Fecha de nacimiento
    fecha_nacimiento = models.DateField(
        help_text="Formato: AAAA-MM-DD"
    )

    # 📚 Grado académico
    grado = models.CharField(
        max_length=20,
        help_text="Ejemplo: 5to grado, Primero de secundaria"
    )

    # 📅 Fecha de registro
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.grado}"

    def edad(self):
        """Calcula la edad del estudiante"""
        from datetime import date
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )