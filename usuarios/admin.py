from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    # Esto hace que la cédula y especialidad salgan en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Médica (Solo para Doctores)', {'fields': ('cedula', 'especialidad', 'telefono', 'es_activo')}),
    )
    # Esto hace que se vean en la lista principal
    list_display = ('username', 'first_name', 'last_name', 'cedula', 'is_staff')

admin.site.register(Usuario, UsuarioAdmin)