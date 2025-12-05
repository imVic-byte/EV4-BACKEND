from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Usuario, Departamento
from .serializers import DepartamentoCreateSerializer, UsuarioSerializer, DepartamentoSerializer, RegisterSerializer
from auditoria.serializers import EventoSerializer
from usuarios.permissions import Admin
import requests

AUDITORIA_API = 'http://localhost:8000/api/eventos/eventos/'

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated, Admin]

    def perform_create(self, serializer):
        serializer.save()
        validated_data = {
            'usuario': self.request.user.id,
            'accion': 'Creación-Departamento',
            'estado': 'permitido'
        }
        print(json=validated_data)
        print("----------------")
        requests.post(AUDITORIA_API, json=validated_data)
    
    def perform_update(self, serializer):
        serializer.save()
        validated_data = {
            'usuario': self.request.user.id,
            'accion': 'Actualización-Departamento',
            'estado': 'permitido'
        }
        requests.post(AUDITORIA_API, json=validated_data)
    
    def perform_destroy(self, serializer):
        serializer.delete()
        validated_data = {
            'usuario': self.request.user.id,
            'accion': 'Eliminación-Departamento',
            'estado': 'permitido'
        }
        requests.post(AUDITORIA_API, json=validated_data)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        validated_data = {
            'usuario': self.request.user.id,
            'accion': 'Creación-Usuario',
            'estado': 'permitido'
        }
        requests.post(AUDITORIA_API, json=validated_data)
    
    def perform_update(self, serializer):
        serializer.save()
        validated_data = {
            'usuario': self.request.user.id,
            'accion': 'Actualización-Usuario',
            'estado': 'permitido'
        }
        requests.post(AUDITORIA_API, json=validated_data)
    
    def perform_destroy(self, serializer):
        serializer.delete()
        validated_data = {
            'usuario': self.request.user.id,
            'accion': 'Eliminación-Usuario',
            'estado': 'permitido'
        }
        requests.post(AUDITORIA_API, json=validated_data)

class UserCreateApiView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
        validated_data = {
            'usuario': None,
            'accion': 'Creación-Usuario',
            'estado': 'permitido'
        }
        requests.post(AUDITORIA_API, json=validated_data)

class DepartamentoCreateApiView(generics.CreateAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
        validated_data = {
            'usuario': None,
            'accion': 'Creación-Departamento',
            'estado': 'permitido'
        }
        requests.post(AUDITORIA_API, json=validated_data)