from django.shortcuts import render

# Create your views here.
# marketplace/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer

@api_view(['POST'])
def create_message(request):
    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_messages(request):
    if request.method == 'GET':
        messages = Message.objects.all()  # Obtener todos los registros del modelo Message
        serializer = MessageSerializer(messages, many=True)  # Serializar los datos obtenidos
        return Response(serializer.data)

@api_view(['GET', 'PUT','DELETE'])
def detail_message(request, pk):
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Se actualizó el estado de la solicitud','id':message.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        message_id = message.id
        message.delete()
        return Response({'message': f'mensaje eliminada','id':message_id}, status=status.HTTP_204_NO_CONTENT)