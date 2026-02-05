from django.db import models
from django.core.validators import RegexValidator

class Padre(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    correo = models.EmailField(
        unique=True,
        error_messages={
            "unique": "Ya existe un padre registrado con este correo."
        }
    )

    documento = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]+$',
                message='El documento solo debe contener números.'
            )
        ]
    )

    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
