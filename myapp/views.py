from django.shortcuts import render

# Create your views here.

# 시간 관련
from datetime import timedelta, datetime
from django.utils import timezone
import pytz

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
from django.contrib import auth
from rest_framework.authtoken.models import Token

from myapp.ollocuser import UserMod

import json

class AuthViewSet(viewsets.ViewSet):
    VALIDATE = 3

    def list(self, request):
        return Response({'message': 'list'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        # 로그인 처리
        try:
            user = auth.authenticate(request, username=request.data['username'], password=request.data['password'])
        except KeyError:
            return Response({'error_code': '0', 'error_msg': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        if user != None:
            token, _ = Token.objects.get_or_create(user=user)

            d = timedelta(days=self.VALIDATE)

            start = (token.created).replace(tzinfo=pytz.UTC)
            dest = (datetime.now()).replace(tzinfo=pytz.UTC)
            end = (token.created + d).replace(tzinfo=pytz.UTC)

            if start > dest or dest > end:
                token.delete()
                return Response({"message": "Token expiration"}, status=status.HTTP_401_UNAUTHORIZED)

            token.created = timezone.now()
            token.save()

            response = {"token": token.key, "created": token.created}

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'error_code': '1', 'error_msg': 'Auth fail'}, status=status.HTTP_401_UNAUTHORIZED)



class UserViewSet(viewsets.ViewSet):
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    """

    usermod = UserMod()

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def list(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token == None:
            return Response({'message': 'None token'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = Token.objects.get(key=token)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_401_UNAUTHORIZED)

        user = token.user

        return Response({'message': 'list'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        try:
            response_msg = self.usermod.add(username=request.data['username'], password=request.data['password'],
                                            name=request.data['name'], mail=request.data['mail'])
        except KeyError:
            return Response({'error_code': 0, 'error_msg': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)
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
