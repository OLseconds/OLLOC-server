from django.db import models
import re


class User:
    def __init__(self, database):
        self.database = database

    def user_profile(self, username):
        # 유저정보 & 가입여부 체크 메서드
        return self.database.user_coll.find_one({"username":username})

    def username_validation(self, username):
        '''
        회원 아이디 유효성 검사 메서드
        :param username: user id
        :return: True is available username
        '''
        return re.sub('[^a-zA-Z0-9_]', ' ', username).strip() == username

    def useradd(self, username, password, name, mail):
        '''
        회원가입 메서
        :param username: join user id
        :param password: join user password
        :param name: join user name
        :param mail: join user e-mail ex) test@test.com
        :return:
        '''

        if not self.username_validation(username):
            return False, 1
        elif self.user_profile(username):
            return False, 2
        else:
            self.database.user_coll.insert_one({
                "username": username,
                "password": password,
                "name": name,
                "mail": mail
            })
            return True

    def change_profile(self):
        # 회원정보 변경
        pass

    def exit_profile(self):
        # 회원 탈퇴
        pass


# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name="회원 아이디", max_length=30)
    password = models.CharField(verbose_name="회원 패스워드", max_length=30)
    name = models.CharField(verbose_name="회원 이름", max_length=15)
    mail = models.CharField(verbose_name="회원 이메일", max_length=30)


class Post(models.Model):
    first_name = models.CharField(verbose_name="이름", max_length=30)
    last_name = models.CharField(verbose_name="성", max_length=30)

