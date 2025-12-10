from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import AllowAny

# Create your views here.

class InfoViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        data = {
            "autor": "[Agregar Autor]",
            "asignatura": "Programación Back End",
            "proyecto": "",
            "description": "",
            "version": "1.0.0",
        }
        return Response(data)