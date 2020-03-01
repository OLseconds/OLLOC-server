from myapp.models import User
from myapp.serializers import UserSerializer
from django.contrib.auth.models import User as authUser

from rest_framework import status
import re

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