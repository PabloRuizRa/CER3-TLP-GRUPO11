from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .forms import RegistroProduccionForm
from .models import RegistroProduccion
from .serializers import RegistroProduccionSerializer
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.db.models import Sum
from django.utils import timezone
from django.conf import settings

def enviar_notificacion_slack(producto_codigo, planta_codigo, litros_producidos, litros_totales):
    print(f"SLACK_TOKEN: {settings.SLACK_TOKEN}")
    print(f"SLACK_CHANNEL: {settings.SLACK_CHANNEL}")
    client = WebClient(token=settings.SLACK_TOKEN)
    message = f"{timezone.now()} {planta_codigo} – Nuevo Registro de Producción – {producto_codigo} {litros_producidos} litros registrados | Total Almacenado: {litros_totales}"
    try:
        response = client.chat_postMessage(channel=settings.SLACK_CHANNEL, text=message)

    except SlackApiError as e:
        print(f"Error al enviar notificación: {e.response['error']}")
from django.contrib import messages

def home(request):
    return render(request, 'core/index.html')


def registrar_produccion(request):
    if request.method == 'POST':
        form = RegistroProduccionForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            combustible = form.cleaned_data['combustible']
            registro.combustible = combustible
            registro.operador = request.user
            registro.save()
            messages.success(request, 'La producción se ha registrado correctamente.')
            return redirect(registrar_produccion)
            total_litros_producidos = RegistroProduccion.objects.filter(combustible=combustible).aggregate(total=Sum('litros_producidos'))['total']
            enviar_notificacion_slack(combustible.codigo, combustible.planta.codigo, registro.litros_producidos, total_litros_producidos)
            return redirect('core/registro_exitoso')
    else:
        form = RegistroProduccionForm()
    return render(request, 'core/registrar_produccion.html', {'form': form})


class RegistroProduccionViewSet(viewsets.ModelViewSet):
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer
    filterset_fields = ['fecha_produccion', 'turno', 'operador', 'combustible']
