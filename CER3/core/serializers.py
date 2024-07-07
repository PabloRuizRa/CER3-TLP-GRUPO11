from rest_framework import serializers
from .models import RegistroProduccion

class RegistroProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroProduccion
        fields = '__all__'