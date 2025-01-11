from django.db import models
from django.contrib.auth.models import User

class Medicion(models.Model):
    sector = models.CharField(max_length=20)
    medida = models.FloatField()
    fecha_hora = models.CharField(max_length=20)
    tecnico= models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.sector} el dia {self.fecha_hora}'