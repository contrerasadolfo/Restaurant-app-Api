from rest_framework import viewsets
from django.db.models import Prefetch
from core.models import Country
from .serializers import CountrySerializer
    
    
class CountryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch('cities')
            )
        return queryset