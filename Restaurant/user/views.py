from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from user.serializers import UserSerializer, AuthSerializer
from cliente.serializers import ClienteSerializer

from core import models

class CreateUserView(generics.CreateAPIView):
    """Crear un nuevo usuario en el sistema"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Crear un nuevo token para el Usuario"""
    serializer_class = AuthSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)



        return Response({
            'token': token.key,
            'id': user.id,
            'nombre': user.nombre,
            'apellido': user.apellido,
            'tipo': user.tipo_user,
            'correo': user.email,

        })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Admin para la autenticacion del usuario"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Recuperar y retornar el usuario autenticado"""
        return self.request.user
