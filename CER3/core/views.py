from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework import viewsets
from .forms import RegistroProduccionForm, RegistroAuditoriaActualizacionForm
from .models import RegistroProduccion
from .serializers import RegistroProduccionSerializer
from django.utils import timezone
from .forms import Creacion_de_usuario
from django.contrib import messages

def home(request):
    es_operador = request.user.groups.filter(name='Operador').exists()
    es_supervisor = request.user.groups.filter(name='Supervisor').exists()
    return render(request, 'core/index.html',  {'es_operador':es_operador, 'es_supervisor':es_supervisor})


def group_required(*group_names):

    def check(user):
        if user.groups.filter(name__in=group_names).exists()    | user.is_superuser:
            return True
        else:
            return False
    return user_passes_test(check, login_url='core/index.html')

@login_required
@group_required('Administrador')
def crear_usuario(request):
    if request.method == 'POST':
        form = Creacion_de_usuario(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Crear el usuario pero no guardarlo aún

            # Obtener el grupo del formulario
            group = form.cleaned_data.get('group')

            if group is not None:
                user.save()  # Guardar el usuario para obtener un ID

                # Asignar el grupo al usuario después de guardarlo
                user.groups.add(group)
                user.save()  # Guardar el usuario nuevamente para aplicar los cambios

                return HttpResponse(f"Usuario {user.username} (ID: {user.id}) ha sido creado y asignado al grupo {group.name}.")
            else:
                return HttpResponse("Error: No se seleccionó un grupo válido.")
    else:
        form = Creacion_de_usuario()
    return render(request, 'registration/crear_usuario.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('home')

@login_required
@group_required('Operador')
def registrar_produccion(request):
    if request.method == 'POST':
        form = RegistroProduccionForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.operador = request.user
            registro.save()
            messages.success(request, 'La producción se ha registrado correctamente.')
            return redirect(registrar_produccion)
    else:
        form = RegistroProduccionForm()
    es_operador = request.user.groups.filter(name='Operador').exists()
    return render(request, 'core/registrar_produccion.html', {'form': form, 'es_operador':es_operador})


@login_required
@group_required('Operador')
def registros(request):
    es_operador = request.user.groups.filter(name='Operador').exists()
    return render(request, 'core/mis_registros.html', {'es_operador':es_operador})


@login_required
@group_required('Operador')
def editar_produccion(request, pk):
    registro = get_object_or_404(RegistroProduccion, pk=pk)

    if registro.operador != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este registro.")

    if request.method == 'POST':
        form = RegistroAuditoriaActualizacionForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')
    else:
        form = RegistroAuditoriaActualizacionForm(instance=registro)

    return render(request, 'core/editar_produccion.html', {'form': form})