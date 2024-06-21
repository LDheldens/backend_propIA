from django.db import models

# Create your models here.

class Message(models.Model):
   
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    celular = models.CharField(max_length=15)
    tipo_solicitud = models.CharField(max_length=20)
    mensaje = models.TextField(max_length=300)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=100)
    atendido = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.nombres} {self.apellidos} - {self.tipo_solicitud}'
