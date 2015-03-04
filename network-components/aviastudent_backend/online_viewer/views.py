# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User

from rest_framework import generics, permissions

from online_viewer.serializers import UserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)
        return (permissions.AllowAny(),)
