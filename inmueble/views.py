from django.shortcuts import render
from django.db.models import Q
from openai import OpenAI
import openai
from django.http import JsonResponse
import json
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_property(request):
    user = request.user
    data = request.data
    data['user_id'] = user.id 

    serializer = PropertySerializer(data=data)
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
    
    
    

# vista para la búsqueda de propieades usando IA
api_key = 'sk-proj-PxqsEdiczaUdivgmHFnCT3BlbkFJUO7C3T6L99mMzhJV1mrI'
# api_key = 'sk-proj-SF4aqZ1jFSHTpReG6Wp8T3BlbkFJ2SJchfDsqtjjn4amBiwB'
client = OpenAI(api_key=api_key)
@api_view(["POST"])
def buscar_propiedades(request):
    data = json.loads(request.body)
    user_input = data.get('message')
    print(user_input)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Convierte esta consulta en una sentencia SQL: {user_input}"}
            ],
            temperature=0.8,
            max_tokens=1000
        )

        sql_query = response.choices[0].message['content'].strip()
        print(sql_query)
        # Ejecutar la consulta SQL en la base de datos
        propiedades = Property.objects.raw(sql_query)
        serializer = PropertySerializer(propiedades, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, safe=False)

    

@api_view(['GET'])
def property_list_user(request, pk):
    print('xd',pk)
    try:
        properties = Property.objects.filter(user_id=pk)
        if not properties.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PropertySerializer(properties, many=True)  # Agregar `many=True`
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['GET'])
# def property_list_user(request, pk):
#     try:
#         properties = Property.objects.filter(user_id=pk)
#         serializer = PropertySerializer(properties,many=True)
#         return Response(serializer.data)
#     except Property.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)