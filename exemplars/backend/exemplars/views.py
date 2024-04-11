from rest_framework import viewsets

from .models import Exemplar, Category
from .serializers import ExemplarSerializer, CategorySerializer



class ExemplarViewSet(viewsets.ModelViewSet):
    queryset = Exemplar.objects.all()
    serializer_class = ExemplarSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
