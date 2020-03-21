from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from django.conf import settings

from myapp.token import TokenMod
from myapp.serializers import UserSerializer, PostsSerializer, PostInfoSerializer, FollowersSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from myapp.models import Followers, Profile
from myapp.olloc import *
import os

SERVER_URL = getattr(settings, 'SERVER_URL', 'localhost')

class Auth(viewsets.ViewSet):
    """
        로그인 인증

        ---
        # 내용
            - username : 회원 아이디
            - password : 회원 패스워드
    """
    queryset = authUser.objects.all()
    serializer_class = UserSerializer
    token = TokenMod()
    user = token

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def list(self, request):
        user = self.token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])

        following = Followers.objects.filter(follower=user.id)
        follower = Followers.objects.filter(following=user.id)

        return Response({
            'id': user.id,
            'username': user.username,
            'name': user.last_name,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'profile_img': SNS.profile_img(user.id),
            'follower': len(follower),
            'following': len(following),
        }, status=status.HTTP_200_OK)

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


class UserViewSet(viewsets.ViewSet):
    usermod = UserMod()
    token = TokenMod()

    def list(self, request):
        user_id = request.query_params.get("user_id")

        username = request.query_params.get("username")
        if not user_id:
            u = authUser.objects.get(username=username)
            user_id = u.id

        try:
            user = self.usermod.user_profile(user_id)
        except authUser.DoesNotExist:
            return Response({'error_code': 1, 'error_msg': 'This user does not exist'})

        following = Followers.objects.filter(follower=user_id)
        follower = Followers.objects.filter(following=user_id)

        return Response({
            'id': user.id,
            'username': user.username,
            'name': user.last_name,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'profile_img': SNS.profile_img(user.id),
            'follower': len(follower),
            'following': len(following),
        }, status=status.HTTP_200_OK)

    # 회원정보 수정
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])
        user_id = request.data.get('user_id')

        image = request.data.get('image')
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

        allow_type = ["image/png", "image/jpeg", "image/gif"]

        from PIL import Image

        if image.content_type in allow_type:
            import hashlib

            og_filename = str(image).split(".")
            types = og_filename[len(og_filename) - 1]
            hash_filename = hashlib.md5(str(image).encode("utf-8")).hexdigest() + "." + types
            path = default_storage.save(os.getcwd() + "/images/" + hash_filename, ContentFile(image.read()))
            url = path.replace(os.getcwd(), "")
            im = Image.open("." + url)
            x, y = im.size
            if x > y:
                new_size = x
                x_offset = 0
                y_offset = int((x - y) / 2)
            elif x < y:
                new_size = y
                x_offset = int((y - x) / 2)
                y_offset = 0

            if x != y:
                new_image = Image.new("RGB", (new_size, new_size), "white")
                new_image.paste(im, (x_offset, y_offset))
                new_image.save("." + url)
        else:
            return {'error_code': 1, 'error_msg': 'Upload file format is incorrect', "error_file": str(image)}, \
                   status.HTTP_400_BAD_REQUEST

        profile = Profile(user_id=user_id, profile_img=url)
        profile.save()

        return Response({"msg": "success"}, status.HTTP_200_OK)

    # 회원가입
    def put(self, request):
        try:
            response_msg = self.usermod.add(username=request.data['username'], password=request.data['password'],
                                            name=request.data['name'], mail=request.data['mail'])
        except KeyError:
            return Response({'error_code': 0, 'error_msg': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_msg[0], status=response_msg[1])

    def delete(self, request):
        # 탈퇴 따위 불가능
        return Response({'message': 'get'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostView(viewsets.ViewSet):
    usermod = UserMod()
    snsmod = SNS()

    serializer_class = PostsSerializer

    # 게시물 가져오기
    def list(self, request):
        # 토큰 인증
        token = TokenMod()
        user = token.tokenAuth(request)
        user_id = 0
        if str(type(user)) != "<class 'tuple'>":
            user_id = user.id

        post_id = request.query_params.get("post_id")

        if post_id is None:
            return Response({'error_code': 0, 'error_msg': "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return_dict = self.snsmod.get_post(post_id, is_like_user=user_id)
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


class Comment(viewsets.ViewSet):
    serializer_class = CommentsSerializer
    queryset = Comments
    snsmod = SNS()

    # 댓글 가져오기
    def list(self, request):
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


class FollowViewSet(viewsets.ViewSet):
    # serializer_class = FollowersSerializer
    # queryset = Followers
    snsmod = SNS()

    def list(self, request):
        token = TokenMod()
        user = token.tokenAuth(request)
        m = request.query_params.get("user_id")

        try:
            search_user_id = user.id if not m and user else m
            is_following_id = user.id if user else False
        except AttributeError:
            search_user_id = m
            is_following_id = False

        re_dict = self.snsmod.follow_list(search_user_id, is_following_id=is_following_id)

        return Response(re_dict, status.HTTP_200_OK)

    # 팔로우 하기
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])

        following = request.data.get("user_id")

        if not following:
            return Response({'error_code': 0, 'error_msg': "Missing parameters"}, status.HTTP_400_BAD_REQUEST)
        try:
            following_id = authUser.objects.get(id=following)
            f = Followers.objects.get_or_create(follower=user.id, following=following)

            return Response({'message': "success"}, status.HTTP_200_OK)
        except authUser.DoesNotExist:
            return Response({'error_code': 1, 'error_msg': "Following target is invalid"}, status.HTTP_400_BAD_REQUEST)

    # 언 팔로우 하기
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def delete(self, request):
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])

        unfollowing = request.query_params.get("user_id")

        if not unfollowing:
            return Response({'error_code': 0, 'error_msg': "Missing parameters"}, status.HTTP_400_BAD_REQUEST)
        try:
            f = Followers.objects.get(follower=user.id, following=unfollowing)
            f.delete()

            return Response({'message': "success"}, status.HTTP_200_OK)
        except authUser.DoesNotExist:
            return Response({'error_code': 1, 'error_msg': "Unfollowing target is invalid"},
                            status.HTTP_400_BAD_REQUEST)
        except Followers.DoesNotExist:
            return Response({'error_code': 2, 'error_msg': "Not Followed target"}, status.HTTP_400_BAD_REQUEST)


class Timeline(viewsets.ViewSet):
    snsmod = SNS()
    serializer_class = TimelineSerializer
    queryset = Posts.objects.all()

    def list(self, request):
        login_user = 0
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) != "<class 'tuple'>":
            login_user = user.id

        user_id = request.query_params.get("user_id")
        start = request.query_params.get("start")
        count = request.query_params.get("count")
        if not start:
            start = 0
        if not count:
            count = 9
        start = int(start)
        count = int(count)

        next_start = int(start) + 9
        next_count = int(count)

        if user_id is not None:
            timeline = self.snsmod.get_userTimeline(user_id, start, count, login_user)
            timelineCount = self.snsmod.get_timelineCount(user_id)

            if timelineCount - next_start < next_count:
                next_count = timelineCount - next_start

            if timelineCount > next_start:
                next_url = SERVER_URL + "/timeline/?user_id=" + str(user_id) + "&start=" + str(next_start) + "&count=" + str(next_count)
            else:
                next_url = False
        else:  # 실제 타임라인 가져오기
            token = TokenMod()
            user = token.tokenAuth(request)
            if str(type(user)) == "<class 'tuple'>":
                return Response(user[0], user[1])

            timelineCount = self.snsmod.get_ftimelineCount(user.id)

            if timelineCount - next_start < next_count:
                next_count = timelineCount - next_start

            if timelineCount > next_start:
                next_url = SERVER_URL + "/timeline/?start=" + str(next_start) + "&count=" + str(next_count)
            else:
                next_url = False

            timeline = self.snsmod.get_followingTimeline(user.id, start, count)

        re_dict = {
            "count": timelineCount,
            "next": next_url,
            "results": timeline,
        }

        return Response(re_dict, status.HTTP_200_OK)



class LikeSet(viewsets.ViewSet):
    snsmod = SNS()

    def list(self, request):
        return Response({'message': "success"}, status.HTTP_405_METHOD_NOT_ALLOWED)

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def put(self, request):
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])

        post_id = request.data.get("post_id")

        if post_id == None:
            return {'error_code': 0, 'error_msg': "Missing parameters"}, status.HTTP_400_BAD_REQUEST

        post = Posts.objects.get(id=post_id)
        if not post:
            return {'error_code': 1, 'error_msg': "Post does not exist"}, status.HTTP_400_BAD_REQUEST
        self.snsmod.like_post(post_id, user.id)

        return Response({'message': "success"}, status.HTTP_200_OK)

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def delete(self, request):
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return Response(user[0], user[1])

        post_id = request.query_params.get("post_id")
        if not post_id:
            return {'error_code': 0, 'error_msg': "Missing parameters"}, status.HTTP_400_BAD_REQUEST
        post = Posts(id=post_id)
        if not post:
            return {'error_code': 1, 'error_msg': "Post does not exist"}, status.HTTP_400_BAD_REQUEST

        self.snsmod.unlike_post(post_id, user.id)

        return Response({'message': "success"}, status.HTTP_200_OK)

# like_post(self, post_id, user_id)
