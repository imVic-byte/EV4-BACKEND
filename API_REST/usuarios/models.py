from django.db import models
from django.contrib.auth.models import User

ROLES_CHOICES = [
    ('admin', 'Administrador'),  
    ('operador', 'Operador'),
]

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    zona = models.CharField(max_length=100)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    rol = models.CharField(max_length=10, choices=ROLES_CHOICES)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
