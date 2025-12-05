from django.db import models
from django.contrib.auth.models import User
from sensores.models import Sensor

class Evento(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True, blank=True)
    accion = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=[('permitido', 'Permitido'), ('denegado', 'Denegado')])