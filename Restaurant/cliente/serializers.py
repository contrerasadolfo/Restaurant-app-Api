from rest_framework import serializers 
from core.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    """Serializador para el object cliente"""
    # photo = serializers.HyperlinkedRelatedField(view_name='media',
    #                                               read_only=True,
    #                                               lookup_field="name",  # Obtenga la dirección relativa del almacenamiento de campo
    #                                               lookup_url_kwarg="path" ) # 
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    photo = serializers.ImageField( max_length=None, use_url=True,)


    class Meta:
        model = Cliente
        fields = ('user','photo') 

    # def validate(self, validated_data):
    #     validated_data['user'] = self.context['request'].user
    #     #other validation logic
    #     return validated_data

    # def create(self, validated_data):
    #     return FileUploader.objects.create(**validated_data)

    
