from django.db import models

class Barrera(models.Model):
    estado = models.BooleanField(default=False)

    def abrir_barrera(self):
        self.estado = True
        self.save()

    def cerrar_barrera(self):
        self.estado = False
        self.save()
        