from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name="회원 아이디", max_length=30, blank=True, null=True)
    password = models.CharField(verbose_name="회원 패스워드", max_length=30, blank=True, null=True)
    name = models.CharField(verbose_name="회원 이름", max_length=15, blank=True, null=True)
    mail = models.CharField(verbose_name="회원 이메일", max_length=30, blank=True, null=True)


class Post(models.Model):
    first_name = models.CharField(verbose_name="이름", max_length=30)
    last_name = models.CharField(verbose_name="성", max_length=30)

    post_id = models.IntegerField(verbose_name="게시물 번호", max_length=)
    owner = models.IntegerField(verbose_name="게시물 소유자", max_length=)
    last_modified = models.DateTimeField(verbose_name="마지막 수정 시간")
    description = models.TextField(verbose_name="게시물 내용")
    contents = models.TextField(verbose_name="사진 및 좌표")
"""

post_id : 게시물 번호 integer
owner : 게시물 소유자 
last_modified : 
description : 게시물 내용
contents: 사진 및 좌표
[
    {
        "image": "https://placehold.it/458x458"
        "location": ["x": 1111, "y": 2222]
    },
    {
        "image": "https://placehold.it/458x458"
        "location": ["x": 1111, "y": 2222]
    },
    {
        "image": "https://placehold.it/458x458"
        "location": ["x": 1111, "y": 2222]
    }
],




"""
