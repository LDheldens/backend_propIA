from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import api_view

@api_view(["GET"])
def ListProperty(request):
    return Response({"testing":"Si funciona get"})

@api_view(["GET"])
def DetailProperty(request,*args,**kwargs):
    return Response({"testing":f"Si funciona get detail {kwargs.get('pk')}"})

@api_view(["POST"])
def CreateProperty(request):
    return Response({"testing":"Si funciona post"})

@api_view(["PUT"])
def UpdateProperty(request,*args,**kwargs):
    return Response({"testing":f"Actualizando {kwargs.get('pk')}"})

@api_view(["DELETE"])
def DeleteProperty(request,*args,**kwargs):
    return Response({"testing":f"Eliminando {kwargs.get('pk')}"})