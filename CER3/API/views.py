from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from core.models import RegistroProduccion
from API.serializers import RegistroProduccionSerializer, ProduccionPorCombustiblePlantaSerializer
from django.db.models import Sum, F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class RegistroProduccionViewSet(viewsets.ModelViewSet):
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer
    filterset_fields = ['fecha_produccion', 'turno', 'operador', 'combustible']
class ProduccionPorCombustiblePlantaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegistroProduccion.objects.annotate(
        combustible_codigo=F('combustible__codigo'),
        planta_codigo=F('combustible__planta__codigo')
    ).values(
        'combustible_codigo', 'planta_codigo'
    ).annotate(
        total_litros_combustible=Sum('litros_producidos')
    )
    serializer_class = ProduccionPorCombustiblePlantaSerializer
    http_method_names = ['get']


class ProduccionPorCombustibleFiltradaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduccionPorCombustiblePlantaSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = RegistroProduccion.objects.annotate(
            combustible_codigo=F('combustible__codigo'),
            planta_codigo=F('combustible__planta__codigo')
        ).values(
            'combustible_codigo', 'planta_codigo'
        ).annotate(
            total_litros_combustible=Sum('litros_producidos')
        )

        # Filtrar por año y mes si están presentes en los parámetros de consulta
        año = self.request.query_params.get('año')
        mes = self.request.query_params.get('mes')

        if año:
            queryset = queryset.filter(fecha_produccion__year=año)
        if mes:
            queryset = queryset.filter(fecha_produccion__month=mes)

        return queryset