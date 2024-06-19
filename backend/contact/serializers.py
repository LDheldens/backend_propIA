
from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'nombres', 'apellidos', 'email', 'celular', 'tipo_solicitud', 'mensaje', 'ciudad', 'provincia', 'codigo_postal']
