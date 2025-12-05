from rest_framework import serializers
from .models import Sensor
from usuarios.models import Departamento

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class DeactivateSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['estado']
    
    def create(self, validated_data):
        raise serializers.ValidationError("Método no admitido.")
    
    def delete(self, instance):
        raise serializers.ValidationError("Método no admitido.")

    def update(self, instance, validated_data):
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()
        return instance

class ActivateSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['estado']
    
    def create(self, validated_data):
        raise serializers.ValidationError("Método no admitido.")
    
    def delete(self, instance):
        raise serializers.ValidationError("Método no admitido.")
    
    def update(self, instance, validated_data):
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()
        return instance