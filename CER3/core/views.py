from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from rest_framework import viewsets
from .forms import RegistroProduccionForm
from .models import RegistroProduccion
from .serializers import RegistroProduccionSerializer
from django.utils import timezone
from .forms import Creacion_de_usuario
from django.contrib import messages

def home(request):
    return render(request, 'core/index.html')


def group_required(*group_names):

    def check(user):
        if user.groups.filter(name__in=group_names).exists()    | user.is_superuser:
            return True
        else:
            return False
    return user_passes_test(check, login_url='incorrect_user/')

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
    return render(request, 'core/registrar_produccion.html', {'form': form})


class RegistroProduccionViewSet(viewsets.ModelViewSet):
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer
    filterset_fields = ['fecha_produccion', 'turno', 'operador', 'combustible']
