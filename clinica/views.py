from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente, NotaMedica, Medicamento, Vacuna 
from .forms import NotaMedicaForm, MedicamentoForm, VacunaForm,PacienteForm #Formularios
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

@login_required
# LISTAR
def lista_pacientes(request):
    # Tomamos lo que el usuario escribió en el buscador (GET).En el html name="q"
    #Si es None, sera una cadena vacia y no aparecera en el buscador
    query = request.GET.get('q') or ""
    if query: # Filtramos por nombre o apellidos que contengan lo que escribio en el nombre o apellido
        pacientes = Paciente.objects.filter(nombre__icontains=query) | Paciente.objects.filter(apellidos__icontains=query) 
    else: # Si no hay búsqueda, mostramos todos los activos 
        pacientes = Paciente.objects.filter(es_activo=True) 
    
    return render(request, 'clinica/lista_pacientes.html', {'pacientes': pacientes, 'query': query})

@login_required
# CREAR
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'clinica/crear_paciente.html', {'form': form})

@login_required
# EDITAR
def editar_paciente(request, paciente_id):#Requiere de parametro en la url.Es la misma que esta en urls.py
    #Obtener el paciente a traves de su id
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        form.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d'] #formato que esta en forms.py
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'clinica/editar_paciente.html', {'form': form})

@login_required
# ELIMINAR (baja lógica)
def eliminar_paciente(request, paciente_id):#Mismo argumento que esta en urls.py
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        paciente.es_activo = False  # baja lógica
        paciente.save()
        return redirect('lista_pacientes')
    return render(request, 'clinica/eliminar_paciente.html', {'paciente': paciente})

@login_required
# Vista principal del expediente (pantalla con buscador)
def expediente_buscar(request): 
    return render(request, 'clinica/expediente_buscar.html')


#BUSCADOR DEL EXPEDIENTE
@login_required
# Vista que devuelve resultados en JSON 
def buscar_pacientes(request): 
    query = request.GET.get('q', '') 
    resultados = [] 
    if query: 
        #Busqueda por nombre completo, curp,telefono
        pacientes = Paciente.objects.filter( nombre__icontains=query ) | Paciente.objects.filter( apellidos__icontains=query ) | Paciente.objects.filter( curp__icontains=query ) | Paciente.objects.filter( telefono__icontains=query ) 
        for p in pacientes: #Guardamos los resultados de la busqueda
            resultados.append({
                'id': p.id, 
                'nombre': f"{p.nombre} {p.apellidos}", 
                'curp': p.curp, 
                'telefono': p.telefono, 
            }) 
    
    return JsonResponse(resultados, safe=False)

#BUSCADOR DEL CRUD
@login_required
def pacientes_autocomplete(request):
    q = request.GET.get('q', '')
    pacientes = Paciente.objects.filter(nombre__icontains=q)[:5]  # máximo 5 sugerencias
    results = []
    for p in pacientes:
        # Campos que se mostrara en la sugerencia
        results.append({
            "id": p.id,
            "nombre": f"{p.nombre} {p.apellidos}",
            'curp':p.curp,
            "telefono": p.telefono,
        })
    return JsonResponse(results, safe=False)

#Es la pantalla "principal" al entrar al expediente. Es el que muesyta las notas medicas
@login_required
def expediente_notas(request, paciente_id):#Mismo argumento que esta en urls.py
    paciente = get_object_or_404(Paciente, id=paciente_id) #paciente
    
    #Ordenadas por fecha
    notas = NotaMedica.objects.filter(paciente=paciente).order_by('-fecha_hora') #notas medicas
    
    #Ultima nota medica (none si no hay). La mas reciente. La usara base_expediente.html
    ultima_nota=notas.first() 
    # Se la manda a la de notas ya que es la que se abre por defecto
    return render(request, 'clinica/expediente_notas.html', {
        'paciente': paciente,
        'notas': notas,
        'ultima_nota':ultima_nota, #base_expediente.html
    })


@login_required
def expediente_medicamentos(request, paciente_id): #Mismo argumento que esta en urls.py
    paciente = get_object_or_404(Paciente, id=paciente_id) 
    
    #Ordenados por fecha
    medicamentos = Medicamento.objects.filter(paciente=paciente).order_by('-nota_medica__fecha_hora')
    
    # Ultima nota medica (none si no hay). La mas reciente. La usara base_expediente.html
    ultima_nota = NotaMedica.objects.filter(paciente=paciente).order_by('-fecha_hora').first()   
    
    notas = NotaMedica.objects.filter(paciente=paciente).order_by('-fecha_hora') #notas medicas 
    
    return render(request, 'clinica/expediente_medicamentos.html', {
        'paciente': paciente, 
        'medicamentos': medicamentos,
        'ultima_nota':ultima_nota,#base_expediente.html
        'notas':notas,
        }) 


@login_required
def expediente_vacunas(request, paciente_id): 
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Ordenas por fecha
    vacunas = Vacuna.objects.filter(paciente=paciente).select_related(
    'nota_medica').order_by('-fecha_aplicacion')
    # Ultima nota medica (none si no hay). La mas reciente. La usara base_expediente.html
    ultima_nota = NotaMedica.objects.filter(paciente=paciente).order_by('-fecha_hora').first()  
    
    notas = NotaMedica.objects.filter(paciente=paciente).order_by('-fecha_hora') #notas medicas
    
    return render(request, 'clinica/expediente_vacunas.html', {
        'paciente': paciente, 
        'vacunas': vacunas,
        'ultima_nota':ultima_nota,#base_expediente.html
        'notas':notas,
        })


@login_required 
def crear_nota_medica(request, paciente_id): #Mismo argumento que esta en urls.py
    paciente = get_object_or_404(Paciente, id=paciente_id)  
    
    #---GRUPO DE FORMULARIOS---
    #Solo un formulario por defecto se muestra
    #No aparece un checbox para eliminarlo.Solo se agregan
    MedicamentoFormSet = modelformset_factory(Medicamento, form=MedicamentoForm, extra=1, can_delete=False) 
    VacunaFormSet = modelformset_factory(Vacuna, form=VacunaForm, extra=1, can_delete=False) 
    
    #Al presionar el boton guardar nota medica
    if request.method == 'POST': 
        nota_form = NotaMedicaForm(request.POST) #Llenar el formulario con los datos ingresados
        
        #---Se crea un registro de formulario---
        #Se crea con los datos que ingreso, si es la primera vez que abre la pagina es none
        #queryset=El campo esta vacio ya que solo esta lo que el usuario esta escribiendo (si no aparecerian los medicamentos/vacunas viejos)
        #prefix=nombre unico/identificador de dicho formulario 
        medicamento_formset = MedicamentoFormSet(request.POST or None, queryset=Medicamento.objects.none(),prefix="medicamento") #crea un conjunto de formularios de medicamentos con los datos enviados
        
        vacuna_formset = VacunaFormSet(request.POST or None, queryset=Vacuna.objects.none(),prefix="vacuna") ##crea un conjunto de formularios de vacunas con los datos enviados
        
        
        if nota_form.is_valid() and medicamento_formset.is_valid() and vacuna_formset.is_valid(): # Guardar la nota médica 
            nota = nota_form.save(commit=False)
            nota.paciente = paciente #AAsignar la nota al paciente
            nota.doctor = request.user #Asignar la nota al doctor logueado
            
            # Calcular IMC automáticamente si hay peso y estatura
            if nota.peso and nota.estatura and nota.estatura > 0: 
                nota.imc = round(nota.peso / (nota.estatura ** 2), 1) 
            
            #Guardar la nota ahora
            nota.save() 
                
            # Guardar medicamentos válidos 
            for m_form in medicamento_formset: 
                cd = m_form.cleaned_data 
                #ejemplo de lo que contiene cd
                # {'nombre': 'Paracetamol', 'dosis': '500 mg',
                #     'frecuencia': 'cada 8 horas', 'duracion': '5 días', 'indicaciones': ''}
                    
                #Validar que los campos obligatorios se llenen para que guarde
                if cd and cd.get('nombre') and cd.get('dosis') and cd.get('frecuencia') and cd.get('duracion'): 
                    medicamento = m_form.save(commit=False)
                    medicamento.nota_medica = nota 
                    medicamento.paciente = paciente 
                    medicamento.save() #GUARDAR MEDICAMENTO (ya que ya ingreso los campos obligatorios)
                        
            # Guardar vacunas válidas 
            for v_form in vacuna_formset: 
                cd = v_form.cleaned_data 
                #Validar que los campos obligatorios se llenen para que se guarde
                # ejemplo de lo que contiene cd
                # {'nombre': 'Paracetamol', 'dosis': '500 mg',
                #     'frecuencia': 'cada 8 horas', 'duracion': '5 días', 'indicaciones': ''}  
                
                                  
                #Con cd.get('nombre') preguntamos si el campo nombre tiene algo escrito
                if cd and cd.get('nombre') and cd.get('dosis') and cd.get('lote') and cd.get('fecha_aplicacion'): 
                    vacuna = v_form.save(commit=False)
                    vacuna.nota_medica = nota
                    vacuna.paciente = paciente 
                    vacuna.save() #GUARDAR VACUNA (ya que ya ingreso los campos obligatorios)
                        
        # Redirigir al expediente (notas médicas) cuando presiona el boton guardar nota medica 
        return redirect('expediente_notas', paciente_id=paciente.id) 
    
    else: #Cuando entra por primera vez, se muestran los campos vacios
        #---GRUPO DE FORMULARIOS---
        nota_form = NotaMedicaForm() 
        medicamento_formset = MedicamentoFormSet(queryset=Medicamento.objects.none(),prefix="medicamento") 
        vacuna_formset = VacunaFormSet(queryset=Vacuna.objects.none(),prefix="vacuna") 
    
    #Mostrar crear_nota_medica.html
    return render(request, 'clinica/crear_nota_medica.html', { 'nota_form': nota_form, 'medicamento_formset': medicamento_formset, 'vacuna_formset': vacuna_formset, 'paciente': paciente, })



@login_required
def pacientes_autocomplete(request):
    q = request.GET.get('q', '')
    pacientes = Paciente.objects.filter(nombre__icontains=q)[:5]  # máximo 5 sugerencias
    results = []
    for p in pacientes:
        #Campos que se mostrara en la sugerencia 
        results.append({
            "id": p.id,
            "nombre": f"{p.nombre} {p.apellidos}",
            "telefono": p.telefono,
        })
    return JsonResponse(results, safe=False)

#Vista para visualizar la nota medica (solo visualizar)
@login_required
def ver_nota_medica(request, paciente_id, nota_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    nota = get_object_or_404(NotaMedica, id=nota_id, paciente=paciente)
    return render(request, "clinica/ver_nota_medica.html", {
        "paciente": paciente,
        "nota": nota
    })
