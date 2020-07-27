import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


from django.db import IntegrityError, transaction

from rest_framework import serializers



class Country(models.Model):
    name = models.CharField(max_length=55)
    
class City(models.Model):
    name = models.CharField(max_length=55)
    country = models.ForeignKey(
        Country, related_name='cities', blank=True, null=True, on_delete=models.SET_NULL)



class UserManager(BaseUserManager):

    @transaction.atomic
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un nuevo usuario"""
        if not email:
            raise ValueError('Ingresar correo electrónico')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        
        try:
            with transaction.atomic():
                
                user.save(using=self._db) 

                if not user.tipo_user:
                    cliente = Cliente.objects.create(user=user)
                    cliente.save(using=self._db)
                
                else:
                    user.is_superuser = True
                    user.is_staff = True
                    admin = Administrador.objects.create(user=user)
                    user.save(using=self._db)
                    admin.save(using=self._db)
                
                return user
        
        except IntegrityError:
            raise serializers.ValidationError({'error': 'Usuario no registrado'})



    
    def create_superuser(self, email, password):
        """Crear y guardar nuevo super usuario"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado que admite el correo electrónico"""
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    email = models.EmailField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    tipo_user = models.IntegerField(default=0)
    registro = models.DateTimeField(auto_now_add=True)




    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return '%s' % (
            self.email
            )


class Administrador(models.Model):
    user = models.OneToOneField(
        User,
        related_name='ida',
        on_delete=models.CASCADE,
        primary_key = True,
        )
    
    def __str__(self):
        return str(self.user_id)


class Cliente(models.Model):
    user = models.OneToOneField(
        User,
        related_name='idc',
        on_delete=models.CASCADE,
        primary_key = True,
        blank=False,
        null=False
        )
    photo = models.ImageField(blank= True, upload_to="foto/%Y/%m/%D", default = 'media/logoGuzerapp.jpg')

    def __str__(self):
        return self.photo.name
