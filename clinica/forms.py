from django import forms
from .models import Paciente,NotaMedica,Medicamento,Vacuna


#LOS CAMPOS DEBEN SER IGUALES AL DE models.py

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        #Quitamos el campo es_activo
        exclude=['es_activo']
        
        #Forzar al campo fecha_nacimiento para que sea tipo calendario
        widgets = {
            'nombre':forms.TextInput(attrs={
                'class': 'crear_paciente_form_control',
                'placeholder':'Nombre del paciente'
            }),
            
            
            'apellidos':forms.TextInput(attrs={
                'class':'crear_paciente_form_control',
                'placeholder':'Apellidos del paciente'                
            }),
            
            
            #SELECT porque son opciones predefinidas (vienen de models.py)
            'genero':forms.Select(attrs={
                'class':'crear_paciente_form_control'
                
            }),
            
            
            'curp':forms.TextInput(attrs={
                'class':'crear_paciente_form_control',
                'placeholder':'CURP del paciente'
            }),
            
            
            'telefono':forms.TextInput(attrs={
                'class':'crear_paciente_form_control',
                'placeholder':'Teléfono del paciente'
            }),
            
            
            #SELECT porque son opciones predefinidas
            'tipo_sangre':forms.Select(attrs={
                'class':'crear_paciente_form_control',
            }),
            
            
            #type: date para que aparezca el calendario
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'crear_paciente_form_control',
                'type': 'date'
            }), 
            
            
            'alergias':forms.TextInput(attrs={
                'class':'crear_paciente_form_control',
                'placeholder':'Ej. Penicilina,Polen'
            }),
            
            
            #Direccion abarca todo el ancho y es mas grande
            'direccion':forms.Textarea(attrs={
                'class':'crear_paciente_form_control direccion-input',
                'placeholder':'Dirección del paciente',
                'rows':2,
                
            })
            
            }
        

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
