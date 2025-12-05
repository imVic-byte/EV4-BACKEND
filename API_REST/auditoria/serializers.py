from rest_framework import serializers
from .models import Evento
from django.contrib.auth.models import User
from sensores.models import Sensor

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['fecha', 'usuario', 'sensor', 'accion', 'estado']

    def validate_accion(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "La acción debe tener al menos 3 caracteres."
            )
        if len(value) > 100:
            raise serializers.ValidationError(
                "La acción no puede exceder 100 caracteres."
            )
        return value.strip()
    
    def validate_estado(self, value):
        estados_validos = ['permitido', 'denegado']
        if value not in estados_validos:
            raise serializers.ValidationError(
                f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
            )
        return value
    
    def validate_usuario(self, value):
        if value and not User.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                "El usuario especificado no existe."
            )
        return value
    
    def validate_sensor(self, value):
        if value and not Sensor.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                "El sensor especificado no existe."
            )
        return value
    
    def validate(self, attrs):
        accion = attrs.get('accion', '')
        sensor = attrs.get('sensor')
        
        acciones_con_sensor = ['Abrir-Barrera', 'Cerrar-Barrera', 'Intento-Acceso']
        if any(acc in accion for acc in acciones_con_sensor):
            if not sensor:
                raise serializers.ValidationError(
                    "Esta acción requiere un sensor asociado."
                )
        
        return attrs

    def create(self, validated_data):
        evento = Evento.objects.create(**validated_data)
        print(validated_data)
        print("----------------")
        print(evento)
        return evento