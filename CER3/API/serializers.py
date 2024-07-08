from rest_framework import serializers
from core.models import RegistroProduccion

class RegistroProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroProduccion
        fields = '__all__'