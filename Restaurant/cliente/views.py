from rest_framework import generics, mixins, parsers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Cliente
from cliente.serializers import ClienteSerializer 


class BaseRolAttrViewSet(viewsets.GenericViewSet, 
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.RetrieveUpdateAPIView):
    """Base viewset for user owned rol attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # lookup_field = pk


class ClienteViewSet(BaseRolAttrViewSet, ):
    """Manage veterinario in the database"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    lookup_fields = ['pk', 'format']

    def get_object(self):
        qs = self.queryset.filter(user=format)
        return qs 


    # def get_queryset(self, *args, **kwargs):
    #     qs = super(ClienteViewSet, self).get_queryset(*args, **kwargs)
    #     qs = qs.filter(user=format)
    #     return qs
