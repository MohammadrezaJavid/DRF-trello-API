from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadonly


# User List
class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


# User Retrieve / Update / Destroy
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    permission_classes = (IsOwnerOrReadonly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Register(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
