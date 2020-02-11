from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from myapp.models import User, Post
from myapp.serializers import UserSerializer, PostSerializer

from rest_framework.decorators import detail_route, list_route

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer




class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer