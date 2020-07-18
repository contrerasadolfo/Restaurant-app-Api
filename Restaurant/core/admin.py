from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext as _

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'nombre', 'apellido', 'direccion']
    fieldsets = (
        # Seccion Login
        (None, {'fields': ('email', 'password')}),
        # Seccion datos Personales
        (_('Informacion Personal'), {'fields': ('nombre', 'apellido',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Direccion'), {'fields': ('direccion',)}),
        (_('Tipo user'), {'fields': ('tipo_user',)}),
        (_('Import dates'), {'fields': ('last_login',)})
    )
    # Crear usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Administrador)
admin.site.register(models.Cliente)