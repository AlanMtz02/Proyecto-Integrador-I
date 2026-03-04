from django import forms
from .models import Paciente,NotaMedica,Medicamento,Vacuna
from django.forms import modelformset_factory

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        #Quitamos el campo es_activo
        exclude=['es_activo']
        
        #Forzar al campo fecha_nacimiento para que sea tipo calendario
        widgets = {'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}), }
        

# Formulario principal de Nota Médica 
class NotaMedicaForm(forms.ModelForm): 
    class Meta:
        model = NotaMedica 
        # Excluimos paciente, doctor y fecha_hora porque se asignan automáticamente en la vista 
        exclude = ['paciente', 'doctor', 'fecha_hora'] 
        
        
# Formulario de Medicamento 
class MedicamentoForm(forms.ModelForm): 
    class Meta: 
        model = Medicamento 
        fields = ['nombre', 'dosis', 'frecuencia', 'duracion', 'indicaciones'] 
        
# Formulario de Vacuna 
class VacunaForm(forms.ModelForm): 
    class Meta: 
        model = Vacuna 
        fields = ['nombre', 'dosis', 'lote', 'fecha_aplicacion'] 
        widgets = { 'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}), }
    
# Formsets dinámicos
#Extra=Numero inicial de formularios
MedicamentoFormSet = modelformset_factory(Medicamento, form=MedicamentoForm, extra=1,can_delete=True) 

VacunaFormSet = modelformset_factory( Vacuna, form=VacunaForm, extra=1, can_delete=True )
