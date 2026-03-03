from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


class UsuarioAdmin(UserAdmin):
    # Columnas
    list_display = ('username', 'first_name', 'last_name',
                    'cedula', 'especialidad', 'is_staff')

    # Esto es lo que el formulario para meter los campos nuevos
    # Agregamos una sección llamada 'Información Médica'
    fieldsets = UserAdmin.fieldsets + (
        ('Información Médica (Datos del Doctor)', {
            'fields': ('cedula', 'especialidad', 'telefono', 'es_activo')
        }),
    )

    # Campos al crear un usuario nuevo 
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Médica', {
            'fields': ('cedula', 'especialidad', 'telefono', 'es_activo')
        }),
    )


admin.site.register(Usuario, UsuarioAdmin)
