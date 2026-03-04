from django.shortcuts import render, get_object_or_404, redirect
from .models import Paciente, NotaMedica, Medicamento, Vacuna 
from .forms import NotaMedicaForm, MedicamentoFormSet, VacunaFormSet,PacienteForm #Formularios
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

@login_required
# Vista que devuelve resultados en JSON 
def buscar_pacientes(request): 
    query = request.GET.get('q', '') 
    resultados = [] 
    if query: 
        #Busqueda por nombre completo, curp,telefono
        pacientes = Paciente.objects.filter( nombre__icontains=query ) | Paciente.objects.filter( apellidos__icontains=query ) | Paciente.objects.filter( curp__icontains=query ) | Paciente.objects.filter( telefono__icontains=query ) 
        for p in pacientes: #Guardamos los resultados de la busqueda
            resultados.append({ 'id': p.id, 'nombre': f"{p.nombre} {p.apellidos}", 'curp': p.curp, 'telefono': p.telefono, }) 
    
    return JsonResponse(resultados, safe=False)

# Vista detalle del expediente 
# views.py

@login_required
def detalle_paciente(request, paciente_id): #Mismo argumento que esta en urls.py
    #Se reutiliza codigo ya que el expediente abre por defecto el menu notas medicas
    return expediente_notas(request, paciente_id)

@login_required
def expediente_notas(request, paciente_id):#Mismo argumento que esta en urls.py
    paciente = get_object_or_404(Paciente, id=paciente_id)
    notas = NotaMedica.objects.filter(paciente=paciente)
    # Se la manda a la de notas ya que es la que se abre por defecto
    return render(request, 'clinica/expediente_notas.html', {
        'paciente': paciente,
        'notas': notas
    })

@login_required
def expediente_medicamentos(request, paciente_id): #Mismo argumento que esta en urls.py
    paciente = get_object_or_404(Paciente, id=paciente_id) 
    medicamentos = Medicamento.objects.filter(paciente=paciente) 
    return render(request, 'clinica/expediente_medicamentos.html', {'paciente': paciente, 'medicamentos': medicamentos}) 

@login_required
def expediente_vacunas(request, paciente_id): 
    paciente = get_object_or_404(Paciente, id=paciente_id) 
    vacunas = Vacuna.objects.filter(paciente=paciente) 
    return render(request, 'clinica/expediente_vacunas.html', {'paciente': paciente, 'vacunas': vacunas})


@login_required 
def crear_nota_medica(request, paciente_id): #Mismo argumento que en urls.py.Se ocupa porque automaticamente debe estar asignado al paciente que estamos viendo el expediente
    #Obtener el paciente
    paciente = get_object_or_404(Paciente, id=paciente_id) 
    #Al presionar el boton guardar
    if request.method == 'POST': 
        form = NotaMedicaForm(request.POST) #Los campos del formulario se llenan con los datos que puso
        medicamento_formset = MedicamentoFormSet(request.POST, queryset=Medicamento.objects.none()) 
        vacuna_formset = VacunaFormSet(request.POST, queryset=Vacuna.objects.none()) 
        
        if form.is_valid() and medicamento_formset.is_valid() and vacuna_formset.is_valid(): 
            
            # Guardar la nota médica 
            nota = form.save(commit=False) 
            nota.paciente = paciente 
            nota.doctor = request.user #Doctor logueado
            nota.save() 
            
            # Guardar medicamentos completos
            for m_form in medicamento_formset: 
                if m_form.cleaned_data and any(m_form.cleaned_data.values()): 
                    medicamento = m_form.save(commit=False) 
                    medicamento.paciente = paciente #Asociar el medicamento al paciente
                    medicamento.nota = nota #Asociar el medicamento a una nota
                    medicamento.save() 
                    
            # Guardar vacunas completas 
            for v_form in vacuna_formset: 
                if v_form.cleaned_data and any(v_form.cleaned_data.values()): 
                    vacuna = v_form.save(commit=False) 
                    vacuna.paciente = paciente #Asociar la vacuna al paciente
                    vacuna.nota = nota 
                    vacuna.save() 
            
            return redirect('detalle_paciente', paciente_id=paciente.id) 
        
        else: #Formulario no valido
            return render(request, 'clinica/crear_nota_medica.html', {'form': form, 'medicamento_formset': medicamento_formset, 'vacuna_formset': vacuna_formset, 'paciente': paciente})
            
    else:
        form = NotaMedicaForm() #Cuando se abre, los campos estan vacios
        medicamento_formset = MedicamentoFormSet(queryset=Medicamento.objects.none()) 
        vacuna_formset = VacunaFormSet(queryset=Vacuna.objects.none())
        
    return render(request, 'clinica/crear_nota_medica.html', { 'form': form, 'medicamento_formset': medicamento_formset, 'vacuna_formset': vacuna_formset, 'paciente': paciente })