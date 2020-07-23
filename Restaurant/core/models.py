import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un nuevo usuario"""
        if not email:
            raise ValueError('Ingresar correo electrónico')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
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
        )
    

    def __str__(self):
        return str(self.user_id)
