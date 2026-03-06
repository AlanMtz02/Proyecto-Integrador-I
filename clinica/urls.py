from django.urls import path
from . import views

urlpatterns = [  
    # CRUD de pacientes 
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'), 
    path('pacientes/nuevo/', views.crear_paciente, name='crear_paciente'), 
    path('pacientes/<int:paciente_id>/editar/', views.editar_paciente, name='editar_paciente'), 
    path('pacientes/<int:paciente_id>/eliminar/', views.eliminar_paciente, name='eliminar_paciente'), 
    
    # Expediente 
    path('expediente/', views.expediente_buscar, name='expediente_buscar'), 
    path('expediente/buscar/', views.buscar_pacientes, name='buscar_pacientes'), 
    path('expediente/<int:paciente_id>/medicamentos/', views.expediente_medicamentos, name='expediente_medicamentos'), 
    path('expediente/<int:paciente_id>/vacunas/', views.expediente_vacunas, name='expediente_vacunas'),
    path('expediente/<int:paciente_id>/notas/', views.expediente_notas, name='expediente_notas'),#Es la que se abre por defecto. Pantalla "principal" de expediente
    path('expediente/<int:paciente_id>/notas/nueva/', views.crear_nota_medica, name='crear_nota_medica')
    ]
