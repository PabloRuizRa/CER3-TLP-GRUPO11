from rest_framework import serializers
from core.models import RegistroProduccion

class RegistroProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroProduccion
        fields = '__all__'

class ProduccionPorCombustiblePlantaSerializer(serializers.Serializer):
    combustible_codigo = serializers.CharField()
    planta_codigo = serializers.CharField()
    total_litros_combustible = serializers.FloatField()