from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Planta(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Combustible(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=100)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RegistroProduccion(models.Model):
    TURNO_CHOICES = [
        ('AM', 'Mañana'),
        ('PM', 'Tarde'),
        ('MM', 'Noche'),
    ]

    combustible = models.ForeignKey(Combustible, on_delete=models.CASCADE)
    litros_producidos = models.FloatField()
    fecha_produccion = models.DateField(default=timezone.now, editable=False)
    turno = models.CharField(max_length=2, choices=TURNO_CHOICES)
    hora_registro = models.TimeField(auto_now_add=True, editable=False)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.combustible} - {self.combustible} - {self.fecha_produccion} - {self.turno}"


class RegistroAuditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_anulacion = models.DateTimeField(auto_now_add=True)
    registro_produccion_id = models.IntegerField()
    detalle = models.TextField()
    

    def str(self):
        return f"Anulación por {self.usuario.username} el {self.fecha_anulacion}"
    
class RegistroAuditoriaActualizacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)
    registro_produccion_id = models.IntegerField()
    detalle = models.TextField()
    

    def str(self):
        return f"Anulación por {self.usuario.username} el {self.fecha_actualizacion}"