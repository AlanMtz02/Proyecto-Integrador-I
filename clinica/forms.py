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
                'placeholder':'CURP del paciente',
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
                'type': 'date',
            },
                format='%Y-%m-%d'  # formato que entiende el input type="date"
            ), 
            
            
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
        
    def clean_curp(self):
        curp = self.cleaned_data.get('curp')
        if curp and len(curp) != 18:
            raise forms.ValidationError(
                "El CURP debe tener exactamente 18 caracteres.")
        return curp.upper() if curp else curp
        

class NotaMedicaForm(forms.ModelForm):
    class Meta:
        model = NotaMedica
        fields = ['tipo_consulta', 'motivo_consulta', 'peso', 'estatura', 'temperatura',
                  'presion_arterial', 'ritmo_cardiaco', 'exploracion_fisica', 'diagnostico', ]
        #Labels que se muestran en los formularios
        labels={'exploracion_fisica':'Exploración fisica y notas'}
        widgets = {
            'tipo_consulta': forms.Select(attrs={'class': 'nnm-form-control'}),
            'motivo_consulta': forms.Textarea(attrs={'rows': 2, 'class': 'nnm-form-control', 'placeholder': 'Ej. Dolor de cabeza, Chequeo general...'}),
            'peso': forms.NumberInput(attrs={'class': 'nnm-form-control nnm-input-vital', 'placeholder': '70'}),
            'estatura': forms.NumberInput(attrs={'class': 'nnm-form-control nnm-input-vital', 'placeholder': '1.75'}),
            'temperatura': forms.NumberInput(attrs={'class': 'nnm-form-control nnm-input-vital', 'placeholder': '36.5'}),
            'presion_arterial': forms.TextInput(attrs={'class': 'nnm-form-control nnm-input-vital', 'placeholder': '120/80'}),
            'ritmo_cardiaco': forms.NumberInput(attrs={'class': 'nnm-form-control nnm-input-vital', 'placeholder': '80'}),
            'exploracion_fisica': forms.Textarea(attrs={'rows': 3, 'class': 'nnm-form-control', 'placeholder': 'Detalles de la exploración física...'}),
            'diagnostico': forms.Textarea(attrs={'rows': 3, 'class': 'nnm-form-control', 'placeholder': 'Diagnóstico médico...'}),
        }


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'dosis', 'frecuencia', 'duracion', 'indicaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'nnm-form-control', 'placeholder': 'Nombre del medicamento'}),
            'dosis': forms.TextInput(attrs={'class': 'nnm-form-control', 'placeholder': 'Dosis'}),
            'frecuencia': forms.TextInput(attrs={'class': 'nnm-form-control', 'placeholder': 'Ej. Cada 8 horas'}),
            'duracion': forms.TextInput(attrs={'class': 'nnm-form-control', 'placeholder': 'Ej. 5 días'}),
            'indicaciones': forms.Textarea(attrs={'rows': 2, 'class': 'nnm-form-control', 'placeholder': 'Indicaciones adicionales'}),
        }


class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre', 'dosis', 'lote', 'fecha_aplicacion']
        widgets = {
            'nombre': forms.Select(attrs={'class': 'nnm-form-control'}),
            'dosis': forms.Select(attrs={'class': 'nnm-form-control'}),
            'lote': forms.TextInput(attrs={'class': 'nnm-form-control', 'placeholder': 'Número de lote'}),
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date', 'class': 'nnm-form-control'}),
        }
