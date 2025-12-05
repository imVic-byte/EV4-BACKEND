from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from usuarios.models import Usuario

class Admin(BasePermission):
    message = "Se requiere el rol de administrador."

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        try:
            profile = request.user.usuario
            return profile.rol == 'admin'
        except Usuario.DoesNotExist:
            return False

class Operador(BasePermission):
    message = "Se requiere el rol de operador o administrador."

    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        try:
            profile = request.user.usuario
            return profile.rol == 'operador' or profile.rol == 'admin'
        except Usuario.DoesNotExist:
            return False
