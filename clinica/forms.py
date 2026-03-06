from django import forms
from .models import Paciente,NotaMedica,Medicamento,Vacuna

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        #Quitamos el campo es_activo
        exclude=['es_activo']
        
        #Forzar al campo fecha_nacimiento para que sea tipo calendario
        widgets = {'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}), }
        

# ------------------------- # Formulario de Nota Médica # ------------------------- 
class NotaMedicaForm(forms.ModelForm): 
    class Meta: 
        model = NotaMedica 
        #Campos
        fields = [ 'tipo_consulta', 'motivo_consulta', 'peso', 'estatura', 'temperatura', 'presion_arterial', 'ritmo_cardiaco', 'exploracion_fisica', 'diagnostico', ] 
        widgets={
            #tipo consulta con opciones predefinidas. campo forms.select
            'tipo_consulta':forms.Select(attrs={
                #Aqui irian estilos 'class':'campo-select.SELECT porque son opciones predefinidas
            }),
            'motivo_consulta':forms.Textarea(attrs={
                'rows':2,
                'placeholder':'Motivo de consulta',
            }),
            #Signos vitales como entradas de numero. campo NumberInput
            'peso':forms.NumberInput(attrs={
                'placeholder':'Peso (kg)',
            }),
            'estatura':forms.NumberInput(attrs={
                'placeholder':'Estatura (m)',
            }),
            'temperatura': forms.NumberInput(attrs={
                'placeholder': 'Temperatura (°C)'
            }), 
            #Presion arterial como campo TextInput
            'presion_arterial': forms.TextInput(attrs={
                'placeholder': 'Presión Arterial (Ej: 120/80)'
            }), 
            'ritmo_cardiaco': forms.NumberInput(attrs={
                'placeholder': 'Ritmo Cardíaco (bpm)'
            }), 
            'exploracion_fisica': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Exploración física', 
            }), 
            'diagnostico': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Diagnóstico', 
            }),
        }

            #  aplicar estilos CSS con clases personalizadas # Ejemplo:(attrs={ 'class': 'campo-select' })

#-------------------------  # Formulario de Medicamento # ------------------------- 
class MedicamentoForm(forms.ModelForm): 
    class Meta: 
        model = Medicamento 
        #Campos
        fields = ['nombre', 'dosis', 'frecuencia', 'duracion', 'indicaciones']
        widgets = { 'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del medicamento'}), 
                   'dosis': forms.TextInput(attrs={'placeholder': 'Dosis'}), 
                   'frecuencia': forms.TextInput(attrs={'placeholder': 'Frecuencia'}), 
                   'duracion': forms.TextInput(attrs={'placeholder': 'Duración'}), 
                   'indicaciones': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Indicaciones (opcional)'}), } 
        
# ------------------------- # Formulario de Vacuna # ------------------------- 
class VacunaForm(forms.ModelForm): 
    class Meta: 
        model = Vacuna 
        #Campos
        fields = ['nombre', 'dosis', 'lote', 'fecha_aplicacion']
        widgets = { 'nombre': forms.Select(attrs={}),#Opciones predefinidas
                   'dosis': forms.Select(attrs={}), #Opciones predefinidas
                   'lote': forms.TextInput(attrs={'placeholder': 'Lote'}), 
                   'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}), } 
        
        #El campo fecha_aplicacion ya tendrá un calendario gracias a type="date"
