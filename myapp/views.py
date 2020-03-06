from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from myapp.token import TokenMod
from myapp.serializers import UserSerializer, PostsSerializer, PostInfoSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from myapp.olloc import *
from rest_framework.views import APIView
import os

class Auth(APIView):
    """
        로그인 인증

        ---
        # 내용
            - username : 회원 아이디
            - password : 회원 패스워드
    """
    queryset = authUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        return Response({"msg": "hi"}, status=status.HTTP_200_OK)

    def post(self, request):
        '''
            Sample의 list를 불러오는 API postpost
            ---
            # 내용
                - username : 회원 아이디
                - password : 회원 패스워드
        '''
        token = TokenMod()
        tokenResult = token.createToken(request)

        return Response(tokenResult[0], status=tokenResult[1])




class UserViewSet(APIView):
    usermod = UserMod()
    token = TokenMod()

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request):
        user = self.token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])

        return Response({
            'id': user.id,
            'username': user.username,
            'name': user.last_name,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active
        }, status=status.HTTP_200_OK)

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


class PostView(APIView):
    usermod = UserMod()
    snsmod = SNS()

    serializer_class = PostsSerializer
    # 게시물 가져오기
    def get(self, request):
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
        new_post = self.snsmod.write_post(request)

        return Response(new_post[0], new_post[1])

    # 글삭제
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def delete(self, request):
        delete_post = self.snsmod.delete_post(request)

        return Response(delete_post[0], delete_post[1])


class Comment(APIView):
    serializer_class = CommentsSerializer
    snsmod = SNS()

    # 댓글 가져오기
    def get(self, request):
        pass

    # 댓글 쓰기
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        new_comment = self.snsmod.write_comment(request)

        return Response(new_comment[0], new_comment[1])

    # 댓글 삭제
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def delete(self, request):
        pass