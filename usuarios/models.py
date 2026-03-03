from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Campos adicionales para el Doctor (pueden ser nulos para el Admin)
    cedula = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Cédula Profesional")
    especialidad = models.CharField(max_length=100, null=True, blank=True, verbose_name="Especialidad")
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono")
    es_activo = models.BooleanField(default=True, verbose_name="Estatus Activo")

    def __str__(self):
        # Si tiene cédula, se presenta como Doctor, si no, como Admin
        if self.cedula:
            return f"Dr. {self.first_name} {self.last_name}"
        return f"Admin: {self.username}"