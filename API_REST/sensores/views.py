from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Sensor
from .serializers import SensorSerializer, DeactivateSensorSerializer, ActivateSensorSerializer
from usuarios.permissions import Admin, Operador
import requests

AUDITORIA_API = 'http://localhost:8000/api/eventos/eventos/'

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated, Admin]

    def _send_audit_log(self, action_name, instance=None, old_data=None):
        
        instance_id = instance.id if instance else 'N/A'
        username = self.request.user.username
        
        audit_data = {
            'usuario': self.request.user.id,
            'accion': action_name,
            'estado': 'permitido',
            'modelo_afectado': 'Sensor',
        }
        try:
            requests.post(AUDITORIA_API, json=audit_data)
        except requests.exceptions.RequestException as e:
            print(f"ERROR DE AUDITORÍA: {e}")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._send_audit_log('Creación-Sensor', instance=instance)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        self._send_audit_log('Actualización-Sensor', instance=instance)
    
    def perform_destroy(self, instance):
        sensor_id = instance.id
        instance.delete()
        self._send_audit_log('Eliminación-Sensor', instance=None)

    @action(detail=True, methods=['patch'], serializer_class=DeactivateSensorSerializer, permission_classes=[IsAuthenticated, Operador])
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={"estado": "inactivo"}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        self._send_audit_log('Desactivación-Sensor', instance=instance)
        
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], serializer_class=ActivateSensorSerializer, permission_classes=[IsAuthenticated, Operador])
    def activate(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={"estado": "activo"}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        self._send_audit_log('Activación-Sensor', instance=instance)

        return Response(serializer.data)
    