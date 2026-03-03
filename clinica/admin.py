from django.contrib import admin
from .models import Paciente, NotaMedica, Medicamento, Vacuna

# Esto permite agregar medicamentos y vacunas dentro de la misma pantalla de la Nota
class MedicamentoInline(admin.TabularInline):
    model = Medicamento
    extra = 1

class VacunaInline(admin.TabularInline):
    model = Vacuna
    extra = 1

#Registrar el  modelo paciente
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    #Columnas
    list_display = ('nombre', 'apellidos', 'curp', 'es_activo')
    #Buscador
    search_fields = ('curp', 'nombre')

#Registrar el modelo nota medica
@admin.register(NotaMedica)
class NotaMedicaAdmin(admin.ModelAdmin):
    #Columnas
    list_display = ('id', 'paciente', 'doctor', 'fecha_hora')
    #Filas/modelos que aparecen dentro de la nota medica
    inlines = [MedicamentoInline, VacunaInline] # Agrega recetas y vacunas directo en la nota