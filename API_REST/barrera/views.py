from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Barrera
from .serializers import BarreraSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sensores.models import Sensor
import requests

AUDITORIA_API = 'http://localhost:8000/api/eventos/eventos/'

class BarreraViewSet(viewsets.ModelViewSet):
    queryset = Barrera.objects.all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def abrir_barrera(self, request, pk=None):
        sensor = Sensor.objects.get(mac=request.data['mac'])
        if sensor.is_active():
            barrera = self.get_object()
            barrera.abrir_barrera()
            validated_data = {
                'usuario': request.user.id,
                'accion' : 'Abrir-Barrera',
                'estado' : 'permitido',
                'sensor' : sensor.id
            }
            requests.post(AUDITORIA_API, json=validated_data)
            return Response({'message': 'Barrera abierta'})
        else:
            validated_data = {
                'usuario': request.user.id,
                'accion' : 'Abrir-Barrera',
                'estado' : 'denegado',
                'sensor' : sensor.id
            }
            requests.post(AUDITORIA_API, json=validated_data)
            return Response({'message': 'Sensor inactivo'}, status=400)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def cerrar_barrera(self, request, pk=None):
        sensor = Sensor.objects.get(mac=request.data['mac'])
        if sensor.is_active():
            barrera = self.get_object()
            barrera.cerrar_barrera()
            validated_data = {
                'usuario': request.user.id,
                'accion' : 'Cerrar-Barrera',
                'estado' : 'permitido',
                'sensor' : sensor.id
            }
            requests.post(AUDITORIA_API, json=validated_data)
            return Response({'message': 'Barrera cerrada'})
        else:
            validated_data = {
                'usuario': request.user.id,
                'accion' : 'Cerrar-Barrera',
                'estado' : 'denegado',
                'sensor' : sensor.id
            }
            requests.post(AUDITORIA_API, json=validated_data)
            return Response({'message': 'Sensor inactivo'}, status=400)