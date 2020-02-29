from django.db import models
from django.shortcuts import get_object_or_404

# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name="회원 아이디", max_length=30, blank=False, null=False)
    password = models.CharField(verbose_name="회원 패스워드", max_length=30, blank=False, null=False)
    name = models.CharField(verbose_name="회원 이름", max_length=15, blank=False, null=False)
    mail = models.CharField(verbose_name="회원 이메일", max_length=30, blank=False, null=False)


class Posts(models.Model):
    post_id = models.IntegerField(verbose_name="게시물 번호", blank=False, null=True)
    owner = models.IntegerField(verbose_name="게시물 소유자", blank=False, null=True)
    last_modified = models.DateTimeField(verbose_name="마지막 수정 시간", blank=False, null=True)
    description = models.TextField(verbose_name="게시물 내용", blank=False, null=True)
    contents = models.TextField(verbose_name="사진 및 좌표", blank=False, null=True)
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
