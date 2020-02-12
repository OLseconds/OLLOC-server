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
    A simple ViewSet for listing or retrieving users.
    queryset = User.objects.all()
    serializer_class = UserSerializer
    """
    '''def get(self, request):
        return Response({'message': '신청한 사물함이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        return Response({'message': '신청한 사물함이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)'''

    usermod = UserMod()
    def list(self, request):
        return Response({'message': 'list'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, v):
        return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        print(request.data['username'])
        response_msg = self.usermod.add(username=request.data['username'], password=request.data['password'],
                                        name=request.data['name'], mail=request.data['mail'])
        return Response(response_msg[0], status=response_msg[1])
        #return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)






class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
