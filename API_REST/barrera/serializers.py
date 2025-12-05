from rest_framework import serializers
from .models import Barrera

class BarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrera
        fields = '__all__'

    def validate_estado(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError(
                "El estado debe ser True (abierta) o False (cerrada)."
            )
        return value
    
    def validate(self, attrs):
        if not self.instance and Barrera.objects.exists():
            raise serializers.ValidationError(
                "Ya existe una barrera en el sistema. No se pueden crear múltiples barreras."
            )
        return attrs