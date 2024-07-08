from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .forms import RegistroProduccionForm
from .models import RegistroProduccion
from .serializers import RegistroProduccionSerializer
from django.utils import timezone
from django.contrib import messages

def home(request):
    return render(request, 'core/index.html')


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
