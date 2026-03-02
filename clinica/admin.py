from django.contrib import admin
from .models import Paciente,NotaMedica,Medicamento

#Registramos y a la vez configuramos la forma que se muestra el modelo en el admin
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    # Columnas(nombre de las variables)
    list_display = ('id','nombre', 'apellidos', 'es_activo')
    #Buscador por nombre,apellidos, curp,id
    search_fields = ('nombre', 'apellidos', 'curp','id')


@admin.register(NotaMedica)
class NotaMedicaAdmin(admin.ModelAdmin):
    # Columnas(nombre de las variables)
    list_display = ('id','paciente', 'doctor', 'fecha_hora')

    # Buscador. paciente es la FK y por ende tiene acceso a los campos del modelo Paciente y lo mismo con doctor solo que con el modelo Usuario
    search_fields = ('paciente__nombre', 'paciente__apellidos', 'doctor__username')


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    #Columnas
    list_display = ('id', 'nombre', 'nota_medica', 'dosis') 
    #Buscador
    search_fields = ('id', 'nombre', 'nota_medica__paciente__nombre')
