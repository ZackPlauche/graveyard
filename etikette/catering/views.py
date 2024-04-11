from rest_framework import viewsets, permissions

from .models import Menu, MenuItem
from .serializers import  MenuSerializer, MenuItemSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    lookup_field = 'slug'


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer