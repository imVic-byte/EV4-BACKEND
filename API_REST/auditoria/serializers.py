from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['fecha', 'usuario', 'sensor', 'accion', 'estado']

    def create(self, validated_data):
        evento = Evento.objects.create(**validated_data)
        print(validated_data)
        print("----------------")
        print(evento)
        return evento