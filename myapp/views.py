from django.shortcuts import render

# Create your views here.

# 시간 관련
from datetime import timedelta, datetime
from django.utils import timezone
import pytz

from rest_framework import viewsets
from myapp.models import Posts, PostInfo
from myapp.serializers import UserSerializer, PostsSerializer

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
from django.forms import model_to_dict
from myapp.ollocuser import UserMod

import os


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
                #return Response({"error_code":1, "error_msg": "Token expiration"}, status=status.HTTP_401_UNAUTHORIZED)

            token.created = timezone.now()
            token.save()

            response = {"token": token.key, "created": token.created}

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'error_code': '2', 'error_msg': 'Auth fail'}, status=status.HTTP_401_UNAUTHORIZED)
    def options(self, request):
        print(request)
        return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ViewSet):

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

        print(request.data)
        try:
            response_msg = self.usermod.add(username=request.data['username'], password=request.data['password'],
                                            name=request.data['name'], mail=request.data['mail'])
        except KeyError:
            return Response({'error_code': 0, 'error_msg': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_msg[0], status=response_msg[1])
    def delete(self, request):
        # 탈퇴 따위 불가능
        return Response({'message': 'get'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostsViewSet(viewsets.ViewSet):
    # queryset = Posts.objects.all()
    # serializer_class = PostsSerializer
    usermod = UserMod()
    # 개인 타임라인 가져오기
    def list(self, request):
        return Response({'message': 'list'}, status=status.HTTP_401_UNAUTHORIZED)

    # 특정 사용자 타임라인 가져오기
    def get(self, v):
        return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)

    # 글 수정 & 글쓰기
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token == None:
            return Response({'error_code': -1, 'error_msg': 'None token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = Token.objects.get(key=token)
        except Exception as ex:
            return Response({'error_code': -1, 'error_msg': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

        # 여기부터 글 쓰기
        user = token.user

        # 필수 파라미터 검사
        for x in ["lx","ly","image","content"]:
            if not request.data.get(x):
                return Response({'error_code': 0, 'error_msg': "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        # 이미지 업로드 처리
        images = request.data.getlist('image')
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

        allow_type = ["image/png", "image/jpeg", "image/gif"]
        uploaded_images = []
        for file in images:
            if file.content_type in allow_type:
                path = default_storage.save(os.getcwd() + "/images/" + str(file), ContentFile(file.read()))
                uploaded_images.append(path.replace(os.getcwd(), ""))
            else:
                return Response({'error_code': 3, 'error_msg': 'Upload file format is incorrect', "error_file":str(file)}, status=status.HTTP_400_BAD_REQUEST)

        lX = request.data.getlist('lx')
        lY = request.data.getlist('ly')

        contxt = request.data.get("content")

        # 글쓰기
        new_post = Posts.objects.create(owner=user.id, description=contxt)

        # 파일 및 지도 기록
        for i in range(len(lX)):
            PostInfo.objects.create(post_id=new_post.id, lx=lX[i], ly=lY[i], img=uploaded_images[i])

        return Response({'message': 'success'}, status=status.HTTP_200_OK)






    # 글쓰기
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def put(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token == None:
            return Response({'message': 'None token'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = Token.objects.get(key=token)
        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_401_UNAUTHORIZED)

        user = token.user
        return Response({'message': 'ㅅㄷㄴㅅ'}, status=status.HTTP_401_UNAUTHORIZED)

    # 글삭제
    def delete(self, request):
        return Response({'message': 'get'}, status=status.HTTP_401_UNAUTHORIZED)
