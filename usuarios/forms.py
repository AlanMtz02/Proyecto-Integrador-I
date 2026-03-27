from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

#Formulario del doctor
#Se usa UserCreationForm debido a que ya trae la logica de de usuarios:validacion de contraseñas, hashing,etc
class RegistroDoctorForm(UserCreationForm):
    #Ya tiene username,password
    nombre=forms.CharField(max_length=30,label="Nombre(s)")
    apellidos=forms.CharField(max_length=150,label="Apellidos")
    
    #--- Configuracion del formulario ---
    class Meta:
        model=Usuario #Asociar el formulario al modelo
        
        fields=['nombre','apellidos','username','password1','password2']
        
        
    #--- Validaciones ----
        
    #Validar que no ingrese un nombre de usuario que ya existe
    #Siempre es clean_*nombredelcampo*
    def clean_username(self):
        #1. Obtener lo que escribio en el campo username
        username=self.cleaned_data.get('username')
        
        #2. Si ya esta en uso por otro usuario mandar error
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
            
        #3. Siempre regresar algo (el campo validado)
        return username
    
    
    #Validar que se guarde en la base de datos
    #Es lo que se ejecuta cuando hace form.save() en la view
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.first_name = self.cleaned_data["nombre"]
        usuario.last_name = self.cleaned_data["apellidos"]
        if commit:
            usuario.save()
        return usuario
    