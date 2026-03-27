from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegistroDoctorForm

# Create your views here.

def registrar_doctor(request):
    
    #Cuando presiona el boton 'Registrar'
    if request.method=="POST":
        form=RegistroDoctorForm(request.POST)
        
        #Validar datos. Se ejecuta la funcionclean_username tambien
        if form.is_valid():
            form.save()
            messages.success(request,"Doctor registrado existosamente. Ya puede iniciar sesión.")
            return redirect('login')#Ya esta habilitado por defecto por usar el login por defecto de django
            
       
    #Aun no presiona el boton registrar, pero esta viendo el formulario 
    else:
        form=RegistroDoctorForm()
        
    return render(request,'clinica/registrar_doctor.html',{
        'form':form
    })