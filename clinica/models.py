from django.db import models

#Nombre en la base de dato: clinica_paciente
class Paciente(models.Model):
    
    # Opciones para el Género
    #El primer valor lo guarda en la base de datos
    #El segundo valor  es lo que se ve en el HTML o en el panel de admin
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    SANGRE_CHOICES = [
        ('O+', 'O Positivo'),
        ('O-', 'O Negativo'),
        ('A+', 'A Positivo'),
        ('A-', 'A Negativo'),
        ('B+', 'B Positivo'),
        ('B-', 'B Negativo'),
        ('AB+', 'AB Positivo'),
        ('AB-', 'AB Negativo'),
    ]
    
    #---COLUMNAS DE LA TABLA---
    #id-->Se genera automaticamente, es autoincrementable y PRIMARY KEY
    curp = models.CharField(max_length=18, unique=True, verbose_name="CURP") #Es unico (no se puede repetir)
    nombre = models.CharField(max_length=100, verbose_name="Nombre(s)")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name="Género")#Solo 1 respuesta y las opciones marcadas
    direccion = models.TextField(verbose_name="Dirección Completa")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono",blank=True,null=True)#Opcional
    tipo_sangre = models.CharField(max_length=3,choices=SANGRE_CHOICES, verbose_name="Tipo de Sangre")
    alergias = models.TextField(verbose_name="Alergias", blank=True, null=True)  # Opcional
    es_activo = models.BooleanField(default=True, verbose_name="Estatus Activo")

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.curp})"
