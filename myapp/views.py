from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from myapp.models import User, Post
from myapp.serializers import UserSerializer, PostSerializer


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from myapp.serializers import UserSerializer, PostSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404


@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
class UserAPI(APIView):

    def get(self, request):
        return Response({'message': '토큰 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        #return Response(User(sheet).data, status.HTTP_200_OK)


    def post(self, request):

        return Response({"test":"test"}, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
        #queryset = User.objects.all()
        #serializer = UserSerializer(queryset, many=True)
        return Response({'message': 'list'}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        return Response({'message': 'retrieve'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        return Response({'message': 'create'}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        return Response({'message': 'update'}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, pk=None):
        return Response({'message': 'partial_update'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        return Response({'message': 'destroy'}, status=status.HTTP_401_UNAUTHORIZED)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
