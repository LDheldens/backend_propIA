from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import api_view
from .models import Blog
from .serializers import BlogSerializer

#Los decoradores se utilizan principalmente para modificar o extender el comportamiento de otras funciones o métodos sin modificar su código fuente.

#El decorador @api_view convierte una función basada en vistas de Django en una vista que puede manejar solicitudes HTTP y generar respuestas HTTP compatibles con DRF.
@api_view(['GET'])
# Define la función getBlogs que acepta una solicitud HTTP request como argumento
def getBlog(request):

    blog = Blog.objects.all()
    # Crea una instancia del serializador BlogSerializer,
    # pasando los objetos blog obtenidos como datos a serializar
    # El parámetro many=True indica que se están serializando varios objetos
    serializer = BlogSerializer(blog, many=True)
    # Devuelve una respuesta HTTP con los datos serializados obtenidos del serializador
    # El método data del serializador devuelve los datos serializados en forma de diccionario Python,
    # que luego se convierte automáticamente a JSON antes de enviarlo como respuesta HTTP
    return Response(serializer.data)

@api_view(['POST'])
def postBlog(request):
    data = request.data
    blog = Blog.objects.create(
        body = data['body']
    )
    serializer = BlogSerializer(blog,many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def putBlog(request, pk):
    # Obtener los datos de la solicitud PUT
    data = request.data
    
    # Obtener el objeto Blog existente de la base de datos mediante su clave primaria (pk)
    blog = Blog.objects.get(id=pk)
    
    # Crear una instancia del serializador BlogSerializer, pasando el objeto Blog existente y los datos de la solicitud
    serializer = BlogSerializer(instance=blog, data=data)
    
    # Verificar si los datos recibidos son válidos según las reglas de validación definidas en el serializador
    if serializer.is_valid():
        # Si los datos son válidos, guardar el objeto actualizado en la base de datos
        serializer.save()
        
        # Devolver una respuesta HTTP con los datos serializados del objeto Blog actualizado
        return Response(serializer.data)
    
@api_view(['DELETE'])
def deleteBlog(request,pk):
    blog = Blog.objects.get(id=pk)
    blog.delete()
    return Response('Blog eliminado')

    
