from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    print(password)
    # Intentar obtener el usuario basado en el correo electrónico
    try:
        user = User.objects.get(email=email)
        print(user.check_password(password))
    except User.DoesNotExist:
        # Si el usuario no existe, devolver un error
        return Response({'error': 'El correo electrónico no está registrado en el sistema'}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(password):
        Token.objects.filter(user=user).delete()
        
        token = Token.objects.create(user=user)
        
        serializer = UserSerializer(instance=user)

        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Contraseña Incorrecta'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():

        user = serializer.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    if user.is_authenticated:  # Verificar si el usuario está autenticado
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    if user.is_authenticated:  # Verificar si el usuario está autenticado
        # Eliminar el token del usuario
        Token.objects.filter(user=user).delete()
        return Response({'message': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Usuario no autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def list_users(request):
    if request.method == 'GET':
        users = User.objects.all()  # Obtener todos los registros del modelo Message
        serializer = UserSerializer(users, many=True)  # Serializar los datos obtenidos
        return Response(serializer.data)
    
@api_view(['PATCH','DELETE'])
def detail_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Se actualizó los datos','id':user.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user_id = user.id
        user.delete()
        return Response({'mensage': f'usuario eliminado','id':user_id}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['PATCH'])
def change_password(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    if 'password' not in request.data:
        return Response({"detail": "La contraseña es requerida."}, status=status.HTTP_400_BAD_REQUEST)
    
    new_password = request.data['password']
    
    # Validación de la longitud de la contraseña
    if len(new_password) < 4:
        return Response({"detail": "La contraseña debe tener al menos 4 caracteres."}, status=status.HTTP_400_BAD_REQUEST)
    
    if check_password(new_password, user.password):
        return Response({"detail": "La nueva contraseña no puede ser la misma que la actual."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Establecer la nueva contraseña
    user.password = make_password(new_password)
    user.save()
    
    return Response({
        'id': user.id,
        'user': {'username': user.username, 'email': user.email},
        'message': 'Se cambió la contraseña',
    }, status=status.HTTP_200_OK)
        