from myapp.serializers import *
from django.contrib.auth.models import User as authUser
from myapp.token import TokenMod
from rest_framework import status
import re, os


class UserMod:
    def __init__(self):
        self.serializer = UserSerializer

    def username_validation(self, username):
        '''
        회원 아이디 유효성 검사 메서드
        :param username: user id
        :return: True is available username
        '''
        return re.sub('[^a-zA-Z0-9_]', ' ', username).strip() == username

    def add(self, username, password, name, mail):
        '''
        회원가입 메서
        :param username: join user id
        :param password: join user password
        :param name: join user name
        :param mail: join user e-mail ex) test@test.com
        :return:
        '''

        if not self.username_validation(username):
            return {"error_code": "1", "error_msg": "Valid username"}, status.HTTP_400_BAD_REQUEST
        try:
            user = authUser.objects.create_user(username=username, password=password, email=mail, last_name=name)
        except Exception as ex:
            return {"error_code": "2", "error_msg": "Username already in use"}, status.HTTP_400_BAD_REQUEST
        return {"msg": "success"}, status.HTTP_200_OK

    def change_profile(self):
        # 회원정보 변경
        pass

    def exit_profile(self):
        # 회원 탈퇴 그런거 없음
        pass

class SNS:
    def __init__(self):
        pass

    def write_post(self, request):
        """

        :param request: body data in HTTP request
        :return: jsondata, HTTP STATUS
        """
        # 토큰 인증
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return user[0], user[1]

        # 필수 파라미터 검사
        for x in ["lx", "ly", "image", "content"]:
            if not request.data.get(x):
                return {'error_code': 0, 'error_msg': "Missing parameters"}, status.HTTP_400_BAD_REQUEST

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
                return {'error_code': 3, 'error_msg': 'Upload file format is incorrect', "error_file": str(file)}, \
                       status.HTTP_400_BAD_REQUEST

        lX = request.data.getlist('lx')
        lY = request.data.getlist('ly')
        mi = request.data.getlist('map_info')

        contxt = request.data.get("content")

        # 글쓰기
        new_post = Posts.objects.create(owner=user.id, description=contxt)

        # 파일 및 지도 기록
        for i in range(len(lX)):
            PostInfo.objects.create(post_id=new_post.id, lx=lX[i], ly=lY[i], map_info=mi[i], img=uploaded_images[i])

        return {'message': 'success'}, status.HTTP_200_OK
    def delete_post(self, request):
        token = TokenMod()
        user = token.tokenAuth(request)
        if str(type(user)) == "<class 'tuple'>":
            return user[0], user[1]

        # 여기부터 글 삭제
        user = token.user
        post_id = request.query_params.get("post_id")

        if post_id is None:
            return {'error_code': 0, 'error_msg': "Missing parameters"}, status.HTTP_400_BAD_REQUEST
        try:
            post_obj = Posts.objects.get(id=post_id)
            if post_obj.owner == user.id:
                # 삭제
                post_obj.delete()
                return {'message': "success"}, status.HTTP_200_OK
            else:
                return {'error_code': 2, 'error_msg': 'post is not yours'}, status.HTTP_400_BAD_REQUEST
        except ValueError:
            return {'error_code': 1, 'error_msg': "Post does not exist"}, status.HTTP_400_BAD_REQUEST

    def delete_post(self, request, post_id):
        if post_id is None:
            return {'error_code': 0, 'error_msg': "Missing parameters"}, status.HTTP_400_BAD_REQUEST
        try:
            post_obj = Posts.objects.get(id=post_id)
            post_obj.delete()
            return {'message': "success"}, status.HTTP_200_OK
        except ValueError:
            return {'error_code': 1, 'error_msg': "Post does not exist"}, status.HTTP_400_BAD_REQUEST