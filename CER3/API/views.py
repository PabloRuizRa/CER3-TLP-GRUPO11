from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroProduccionForm
from rest_framework import generics
from .models import RegistroProduccion
from .serializers import RegistroProduccionSerializer

@login_required
def registrar_produccion(request):
    if request.method == 'POST':
        form = RegistroProduccionForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.operador = request.user
            registro.save()
            return redirect('registro_exitoso')
    else:
        form = RegistroProduccionForm()
    return render(request, 'registro/registrar_produccion.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'registro/registro_exitoso.html')

class RegistroProduccionListCreate(generics.ListCreateAPIView):
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer
    filterset_fields = ['fecha_produccion', 'turno', 'operador', 'combustible']
