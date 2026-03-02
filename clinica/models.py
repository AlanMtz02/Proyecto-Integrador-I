from django.db import models
from usuarios.models import Usuario

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
        return f"{self.nombre} {self.apellidos} (ID: {self.id})"




# Nombre en la base de datos: clinica_notamedica
class NotaMedica(models.Model):
    CONSULTA_CHOICES = [
        ('General', 'Medicina General'),
        ('Especialidad', 'Especialidad'),
        ('Urgencia', 'Urgencia'),
        ('Chequeo', 'Chequeo'),
    ]

    # ---COLUMNAS DE LA TABLA---

    # Relaciones (Llaves foraneas)
    # Vincula la nota con un paciente. Si el paciente se borra, se borran sus notas (on_delete=CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")

    # Vincula con el Doctor que está logueado
    doctor = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, verbose_name="Doctor")

    # Fecha y Hora (automatico)
    fecha_hora = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha y Hora de atención")

    # Tipo de consulta con opciones definidas
    tipo_consulta = models.CharField(
        max_length=20, choices=CONSULTA_CHOICES, verbose_name="Tipo de Consulta")

    motivo_consulta = models.TextField(verbose_name="Motivo de Consulta")

    # Signos Vitales (TODOS OPCIONALES)
    peso = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Peso (kg)", blank=True, null=True)
    estatura = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Estatura (m)", blank=True, null=True)
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, verbose_name="Temperatura (°C)", blank=True, null=True)
    imc = models.DecimalField(
        max_digits=4, decimal_places=1, verbose_name="IMC", blank=True, null=True)
    presion_arterial = models.CharField(
        max_length=20, verbose_name="Presión Arterial", blank=True, null=True)
    ritmo_cardiaco = models.IntegerField(
        verbose_name="Ritmo Cardíaco (bpm)", blank=True, null=True)

    exploracion_fisica = models.TextField(verbose_name="Exploración Física")
    diagnostico = models.TextField(verbose_name="Diagnóstico")

    def __str__(self):
        return f"Nota de {self.paciente} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"


#Nombre en la base de datos: clinica_medicamento
class Medicamento(models.Model):
    
    #---COLUMNAS DE LA TABLA---
    #id-->Se genera automaticamente, autoincrementable y es PRIMARY KEY
    # Relación: Un medicamento pertenece a UNA nota médica específica
    # related name sirve hacer tipo nota_medica.medicamentos.all para obtener todos los medicamentos de esa nota
    nota_medica = models.ForeignKey(
        NotaMedica, on_delete=models.CASCADE, related_name='medicamentos', verbose_name="Nota Médica")
    
    #Todos son campos de texto
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Medicamento")
    dosis = models.CharField(max_length=100, verbose_name="Dosis (Ej: 500mg)")
    frecuencia = models.CharField(max_length=100, verbose_name="Frecuencia (Ej: Cada 8 horas)")
    duracion = models.CharField(max_length=100, verbose_name="Duración del tratamiento (Ej: 7 días)")

    def __str__(self):
        return f"{self.nombre} - {self.nota_medica.paciente.nombre}"