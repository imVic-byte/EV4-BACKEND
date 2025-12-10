from rest_framework import serializers
from .models import Sensor
from usuarios.models import Departamento
import re

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

    def validate_nombre(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El nombre del sensor debe tener al menos 3 caracteres."
            )
        if len(value) > 100:
            raise serializers.ValidationError(
                "El nombre del sensor no puede exceder 100 caracteres."
            )
        return value.strip()
    
    def validate_tipo(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El tipo del sensor debe tener al menos 3 caracteres."
            )
        return value.strip()
    
    def validate_mac(self, value):
        if not value:
            raise serializers.ValidationError("La dirección MAC es obligatoria.")
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if not re.match(mac_pattern, value):
            raise serializers.ValidationError(
                "Formato de MAC inválido. Debe ser XX:XX:XX:XX:XX:XX (ejemplo: AA:BB:CC:DD:EE:FF)"
            )
        value = value.upper()
        if self.instance:
            if Sensor.objects.exclude(pk=self.instance.pk).filter(mac=value).exists():
                raise serializers.ValidationError(
                    f"Ya existe un sensor con la MAC {value}."
                )
        else:
            if Sensor.objects.filter(mac=value).exists():
                raise serializers.ValidationError(
                    f"Ya existe un sensor con la MAC {value}."
                )
        
        return value
    
    def validate_estado(self, value):
        estados_validos = ['activo', 'inactivo', 'bloqueado', 'perdido']
        if value not in estados_validos:
            raise serializers.ValidationError(
                f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
            )
        return value
    
    def validate_departamento(self, value):
        if value and not Departamento.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                "El departamento especificado no existe."
            )
        return value
        
class DeactivateSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['estado']

    def validate_estado(self, value):
        if value != 'inactivo':
            raise serializers.ValidationError(
                "Este endpoint solo permite cambiar el estado a 'inactivo'."
            )
        return value    
    
    def create(self, validated_data):
        raise serializers.ValidationError("Método no admitido.")
    
    def delete(self, instance):
        raise serializers.ValidationError("Método no admitido.")

    def update(self, instance, validated_data):
        if instance.estado == 'bloqueado':
            raise serializers.ValidationError(
                "No se puede desactivar un sensor bloqueado. Desbloquearlo primero."
            )
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()
        return instance

class ActivateSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['estado']

    def validate_estado(self, value):
        if value != 'activo':
            raise serializers.ValidationError(
                "Este endpoint solo permite cambiar el estado a 'activo'."
            )
        return value
    
    def create(self, validated_data):
        raise serializers.ValidationError("Método no admitido.")
    
    def delete(self, instance):
        raise serializers.ValidationError("Método no admitido.")
    
    def update(self, instance, validated_data):
        if instance.estado == 'perdido':
            raise serializers.ValidationError(
                "No se puede activar un sensor reportado como perdido."
            )
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()
        return instance