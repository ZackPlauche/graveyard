from rest_framework import viewsets

from accounts.serializers import UserSerializer
from config.permissions import IsUserOrAdminUserOrReadOnly

from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrAdminUserOrReadOnly]
