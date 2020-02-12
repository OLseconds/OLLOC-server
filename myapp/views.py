from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets
from myapp.models import User, Post
from myapp.serializers import UserSerializer, PostSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


from myapp.ollocuser import UserMod

import json

class UserViewSet(viewsets.ViewSet):
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    """

    usermod = UserMod()
    def list(self, request):
        print(self.usermod.profile("test22"))
        return Response({'message': 'list'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        print(request.data['username'])
        response_msg = self.usermod.add(username=request.data['username'], password=request.data['password'],
                                        name=request.data['name'], mail=request.data['mail'])
        return Response(response_msg[0], status=response_msg[1])


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # 개인 타임라인 가져오기
    def list(self, request):
        return Response({'message': 'list'}, status=status.HTTP_401_UNAUTHORIZED)

    # 특정 사용자 타임라인 가져오기
    def get(self, v):
        return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)

    # 글쓰기
    def post(self, request):
        return Response(response_msg[0], status=response_msg[1])

    # 글삭제
    def delete(self, request):
        return Response(response_msg[0], status=response_msg[1])
