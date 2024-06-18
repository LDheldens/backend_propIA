from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import api_view
from .serializers import PropertySerializer, ImagePropertySerializer
from rest_framework import status
from .models import *

@api_view(["GET"])
def ListProperty(request):
    properties = Property.objects.all()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_property(request):
    return Response({"testing":"Si funciona post"})

@api_view(['GET', 'PUT', 'DELETE'])
def property_detail(request, pk):
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PropertySerializer(property)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'La propiedad se actualizó de manera exitosa','id':property.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        property_id = property.id
        property.delete()
        return Response({'message': f'Propidad eliminada','id':property_id}, status=status.HTTP_204_NO_CONTENT)