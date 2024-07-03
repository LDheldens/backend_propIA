from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import api_view
from .serializers import PropertySerializer, ImagePropertySerializer
from rest_framework import status
from .models import *
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(["GET"])
def ListPropertyAdmin(request):
    properties = Property.objects.all()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def ListProperty(request):
    properties = Property.objects.all()

    property_type = request.query_params.get('type', None)
    search_text = request.query_params.get('text', None)
    type_operation = request.query_params.get('transaction', None)

    if property_type:
        properties = properties.filter(type_property__icontains=property_type)
    
    if search_text:
        properties = properties.filter(
            Q(provincia__icontains=search_text) | 
            Q(description__icontains=search_text) |
            Q(distrito__icontains=search_text)
        )
    
    if type_operation:
        properties = properties.filter(type_operation__icontains=type_operation)

    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(properties, request)
    serializer = PropertySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
def create_property(request):
    print(request.data)  # Para depuración
    print('IMAGENES',request.FILES)  # Para depuración
    serializer = PropertySerializer(data=request.data)
    if serializer.is_valid():
        property_instance = serializer.save()

        # Manejo de las imágenes
        for image in request.FILES.getlist('images'):
            ImageProperty.objects.create(property=property_instance, image=image)
        
        return Response({'message': 'Propiedad registrada de manera exitosa', 'id': property_instance.id}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    

@api_view(['GET'])
def property_list_user(request, pk):
    try:
        properties = Property.objects.get(user_id=pk)
        serializer = PropertySerializer(properties)
        return Response(serializer.data)
    except Property.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
