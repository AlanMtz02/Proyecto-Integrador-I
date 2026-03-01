from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#Nombre en la base de datos: usuarios_usuario
class Usuario(AbstractUser):
    #---Se hereda de un modelo por defecto de django---
    #---COLUMNAS DE LA TABLA---
    #id--> se genera automaticamente, es incrementable y PRIMARY KEY
    # Campos que ya trae AbstractUser:
    # username, password, first_name (Nombre), last_name (Apellidos), email
    
    #Campos adicionales (verbose_name=Nombre que sale en los formularios)
    cedula = models.CharField(max_length=20,unique=True,verbose_name="Cédula Profesional")#unique=No permite que dos doctores tengan la misma cedula
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono de Contacto",blank=True,null=True) #Es opcional
    es_activo = models.BooleanField(default=True, verbose_name="¿Está trabajando actualmente?")
    
    #Util para visualizar datos de manera clara en consola, panel de administrador
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.especialidad}"
    
    
#SIEMPRE QUE SE CREA UN MODELO APLICAR
#python manage.py makemigrations usuarios
# python manage.py migrate

#---CREDENCIALES---
#username: admin
#password: admin2026