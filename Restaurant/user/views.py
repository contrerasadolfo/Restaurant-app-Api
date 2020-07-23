from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthSerializer

class CreateUserView(generics.CreateAPIView):
    """Crear un nuevo usuario en el sistema"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Crear un nuevo token para el Usuario"""
    serializer_class = AuthSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
