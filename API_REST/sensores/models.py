from django.db import models
from usuarios.models import Departamento

class Sensor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    mac = models.CharField(max_length=17, unique=True)
    estado = models.CharField(max_length=10, choices=[
        ('activo', 'Activo'), 
        ('inactivo', 'Inactivo'), 
        ('bloqueado', 'Bloqueado'),
        ('perdido', 'Perdido')
        ])
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)

    def is_active(self):
        return self.estado == 'activo'