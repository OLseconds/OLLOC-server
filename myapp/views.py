from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from myapp.models import Posts, PostInfo
from myapp.token import TokenMod
from myapp.serializers import UserSerializer, PostsSerializer, PostInfoSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from myapp.ollocuser import UserMod

import os


class AuthViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'message': 'bad request'}, status=status.HTTP_400_UNAUTHORIZED)

    def get(self, request):
        return Response({'message': 'bad request'}, status=status.HTTP_400_UNAUTHORIZED)

    def post(self, request):
        token = TokenMod()
        tokenResult = token.createToken(request)

        return Response(tokenResult[0], status=tokenResult[1])


class UserViewSet(viewsets.ViewSet):
    usermod = UserMod()

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def list(self, request):
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
    usermod = UserMod()

    # 게시물 가져오기
    def list(self, request):
        # 토큰 인증
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])
        post_id = request.query_params.get("post_id")

        if post_id is None:
            return Response({'error_code': 0, 'error_msg': "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post_obj = Posts.objects.get(id=post_id)
            ps = PostsSerializer(post_obj)
            postInfo_obj = PostInfo.objects.filter(post_id=ps.data["id"])

            return_dict = ps.data

            for x in postInfo_obj:
                for key, value in PostInfoSerializer(x).data.items():
                    if not key in return_dict:
                        return_dict[key] = []
                    return_dict[key].append(value)

            return Response(return_dict, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error_code': 1, 'error_msg': "Post does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    # 글 수정 & 글쓰기
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        # 토큰 인증
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])

        # 필수 파라미터 검사
        for x in ["lx", "ly", "image", "content"]:
            if not request.data.get(x):
                return Response({'error_code': 0, 'error_msg': "Missing parameters"},
                                status=status.HTTP_400_BAD_REQUEST)

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
                return Response(
                    {'error_code': 3, 'error_msg': 'Upload file format is incorrect', "error_file": str(file)},
                    status=status.HTTP_400_BAD_REQUEST)

        lX = request.data.getlist('lx')
        lY = request.data.getlist('ly')

        contxt = request.data.get("content")

        # 글쓰기
        new_post = Posts.objects.create(owner=user.id, description=contxt)

        # 파일 및 지도 기록
        for i in range(len(lX)):
            PostInfo.objects.create(post_id=new_post.id, lx=lX[i], ly=lY[i], img=uploaded_images[i])

        return Response({'message': 'success'}, status=status.HTTP_200_OK)

    # 글삭제
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def delete(self, request):
        # 토큰 인증
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])

        # 여기부터 글 쓰기
        user = token.user
        post_id = request.query_params.get("post_id")

        if post_id is None:
            return Response({'error_code': 0, 'error_msg': "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post_obj = Posts.objects.get(id=post_id)
            if post_obj.owner == user.id:
                # 삭제
                post_obj.delete()
                return Response({'message': "success"}, status=status.HTTP_200_OK)
            else:
                return Response({'error_code': 2, 'error_msg': 'post is not yours'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error_code': 1, 'error_msg': "Post does not exist"}, status=status.HTTP_400_BAD_REQUEST)
