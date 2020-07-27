from django.conf.urls import url, include
from rest_framework import routers
from cliente import views
from django.urls import path

router =routers.DefaultRouter()
router.register('perfil/foto', views.ClienteViewSet)
app_name = 'cliente'

urlpatterns = [
    path('', include(router.urls)),
]