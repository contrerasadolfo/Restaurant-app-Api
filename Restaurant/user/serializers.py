from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from cliente.serializers import ClienteSerializer 
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializador para el Objeto User"""
    idc = ClienteSerializer(read_only=True)
    class Meta:    
        model = get_user_model()
        fields = ('id','email', 'password', 'nombre', 'apellido', 'direccion', 'tipo_user', 'idc')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}, 'idc':{'read_only':True}}


    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update a user, setting the password correcly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user


class AuthSerializer(serializers.Serializer):
    """Serializador para autenticar usuarios"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password' },
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validacion y autenticacion de usuario"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )

        if not user:
            msg = _('Correo o Contraseña Invalidos')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs



    






