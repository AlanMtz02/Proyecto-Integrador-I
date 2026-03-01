from django.contrib import admin
from .models import Paciente

#Registramos y a la vez configuramos la forma que se muestra el modelo en el admin
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    # Columnas
    list_display = ('nombre', 'apellidos', 'curp', 'es_activo')
    #Buscador por nombre,apellidos, curp,id
    search_fields = ('nombre', 'apellidos', 'curp','id')
