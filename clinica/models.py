from django.db import models
from django.conf import settings
from datetime import date

#clinica_paciente
class Paciente(models.Model):
    #Opciones de genero
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    #Opciones de sangre
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

    #id-->PRIMARY KEY
    curp = models.CharField(max_length=18, unique=True, verbose_name="CURP")#UNICO
    nombre = models.CharField(max_length=100, verbose_name="Nombre(s)")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name="Género")#Opciones predefinidas
    direccion = models.TextField(verbose_name="Dirección Completa")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    tipo_sangre = models.CharField(max_length=3, choices=SANGRE_CHOICES, verbose_name="Tipo de Sangre")#Opciones predefinidas
    alergias = models.TextField(verbose_name="Alergias", blank=True, null=True)#OPCIONAL
    es_activo = models.BooleanField(default=True, verbose_name="Estatus Activo")#Baja logica

    def __str__(self):
        return f"{self.nombre} {self.apellidos} (ID: {self.id})"

    #Funcion que calcula la edad automaticamente. En los html se debe llamar como .edad
    @property
    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (
                self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
#clinica_notamedica
class NotaMedica(models.Model):
    #Opciones para la consulta
    CONSULTA_CHOICES = [
        ('General', 'Medicina General'),
        ('Especialidad', 'Especialidad'),
        ('Urgencia', 'Urgencia'),
        ('Chequeo', 'Chequeo'),
    ]
    
    #id-->PRIMARY KEY
    #Relacion
    # PROTECT: No se puede borrar el paciente o doctor si hay notas
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Paciente")
    # Aquí se guarda el ID del Usuario (Doctor) logueado
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Doctor")
    
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora de atención")#Automaticamente
    tipo_consulta = models.CharField(max_length=20, choices=CONSULTA_CHOICES, verbose_name="Tipo de Consulta")#Opciones predefinidas
    motivo_consulta = models.TextField(verbose_name="Motivo de Consulta")

    # Signos Vitales (Opcionales)
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso (kg)", blank=True, null=True)
    estatura = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Estatura (m)", blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Temperatura (°C)", blank=True, null=True)
    imc = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="IMC", blank=True, null=True)
    presion_arterial = models.CharField(max_length=20, verbose_name="Presión Arterial", blank=True, null=True)
    ritmo_cardiaco = models.IntegerField(verbose_name="Ritmo Cardíaco (bpm)", blank=True, null=True)

    exploracion_fisica = models.TextField(verbose_name="Exploración Física")
    diagnostico = models.TextField(verbose_name="Diagnóstico")

    def __str__(self):
        return f"Nota de {self.paciente} - {self.fecha_hora.strftime('%d/%m/%Y')}"

#clinica_medicamento
class Medicamento(models.Model):
    
    #id-->PRIMARY KEY
    #Relacion
    # CASCADE: Si borras la nota, se borra el medicamento
    nota_medica = models.ForeignKey(NotaMedica, on_delete=models.CASCADE, related_name='medicamentos', verbose_name="Nota Médica")
    # SET_NULL: Si borras al paciente, el medicamento se queda en la nota pero el campo paciente se limpia, queda como desconocido
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True, verbose_name="Paciente")
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Medicamento")
    dosis = models.CharField(max_length=100, verbose_name="Dosis")
    frecuencia = models.CharField(max_length=100, verbose_name="Frecuencia")
    duracion = models.CharField(max_length=100, verbose_name="Duración")
    indicaciones = models.TextField(verbose_name="Indicaciones adicionales", blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.paciente.nombre if self.paciente else 'Sin Paciente'}"


#clinica_vacuna
class Vacuna(models.Model):
    #El primer argumento es como se guarda en la bd y el segundo es la etiqueta legible para el html
    # vacuna_get_campo_display
    # {{vacuna.get_dosis_display}} para obtener el segundo argumento para la dosis
    VACUNA_CHOICES = [
        ('COVID-19', 'COVID-19 (Sars-CoV-2)'),
        ('BCG', 'BCG (Tuberculosis)'),
        ('Hepatitis B', 'Hepatitis B'),
        ('Pentavalente', 'Pentavalente acelular'),
        ('Rotavirus', 'Rotavirus'),
        ('Neumocócica', 'Neumocócica conjugada'),
        ('Influenza', 'Influenza'),
        ('SRP', 'SRP (Sarampión, Rubeola, Parotiditis)'),
        ('Sabin', 'Sabin (Polio)'),
        ('DPT', 'DPT (Difteria, Tos ferina, Tétanos)'),
        ('SR', 'SR (Sarampión y Rubeola)'),
        ('TD', 'Tétanos y Difteria'),
        ('VPH', 'VPH (Virus del Papiloma Humano)'),
    ]
    
    DOSIS_CHOICES = [
        ('Unica', 'Dosis Única'),
        ('1ra', 'Primera Dosis'),
        ('2da', 'Segunda Dosis'),
        ('3ra', 'Tercera Dosis'),
        ('4ta', 'Cuarta Dosis'),
        ('Refuerzo', 'Refuerzo'),
        ('Anual', 'Dosis Anual'),
    ]

    #id-->PRIMARY KEY
    #Relacion
    nota_medica = models.ForeignKey(NotaMedica, on_delete=models.CASCADE, related_name='vacunas', verbose_name="Nota Médica")
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True, verbose_name="Paciente")
    
    nombre = models.CharField(max_length=100, choices=VACUNA_CHOICES, verbose_name="Nombre de la Vacuna")
    dosis = models.CharField(max_length=50, choices=DOSIS_CHOICES, verbose_name="Dosis")
    lote = models.CharField(max_length=50, verbose_name="Número de Lote")
    fecha_aplicacion = models.DateField(verbose_name="Fecha de Aplicación")

    def __str__(self):
        return f"{self.get_nombre_display()} - {self.paciente.nombre if self.paciente else 'Sin Paciente'}"