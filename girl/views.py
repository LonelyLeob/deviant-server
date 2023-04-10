from rest_framework import generics
from .serializers import GirlSerializer
from .models import Girl

class GirlAPIView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = GirlSerializer
    queryset = Girl.objects.all()