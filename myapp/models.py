from django.db import models
from django.shortcuts import get_object_or_404


class User(models.Model):
    username = models.CharField(verbose_name="회원 아이디", max_length=30, blank=False, null=False)
    password = models.CharField(verbose_name="회원 패스워드", max_length=30, blank=False, null=False)
    name = models.CharField(verbose_name="회원 이름", max_length=15, blank=False, null=False)
    mail = models.CharField(verbose_name="회원 이메일", max_length=30, blank=False, null=False)


class Posts(models.Model):
    owner = models.IntegerField(verbose_name="게시물 소유자", blank=False, null=True)
    last_modified = models.DateTimeField(verbose_name="마지막 수정 시간", blank=False, null=True)
    date = models.DateTimeField(verbose_name="글쓴 시간", auto_now_add=True, null=True)
    description = models.TextField(verbose_name="게시물 내용", blank=False, null=True)


class PostInfo(models.Model):
    post_id = models.IntegerField(verbose_name="대상 게시물 ID", blank=False, null=True)
    lx = models.CharField(verbose_name="x좌표", max_length=30, null=True)
    ly = models.CharField(verbose_name="y좌표", max_length=30, null=True)
    map_info = models.TextField(verbose_name="지도 정보", null=True)
    img = models.URLField(verbose_name="이미지 경로", null=True)


class Comments(models.Model):
    post_id = models.IntegerField(verbose_name="대상 게시물 ID", blank=False, null=True)
    owner = models.IntegerField(verbose_name="게시물 소유자", blank=False, null=True)
    description = models.TextField(verbose_name="게시물 내용", blank=False, null=True)
    date = models.DateTimeField(verbose_name="글쓴 시간", auto_now_add=True, null=True)
    last_modified = models.DateTimeField(verbose_name="마지막 수정 시간", blank=False, null=True)


class Follow(models.Model):
    follower = models.IntegerField(verbose_name="팔로워", blank=False, null=True)
    followering = models.IntegerField(verbose_name="팔로잉 한 사람", blank=False, null=True)
    date = models.DateTimeField(verbose_name="팔로우 시간", auto_now_add=True, null=True)

class PushList(models.Model):
    owner = models.IntegerField(verbose_name="팔로잉 한 사람", blank=False, null=True)
    description = models.TextField(verbose_name="게시물 내용", blank=False, null=True)
    link = models.DateTimeField(verbose_name="팔로우 시간", auto_now_add=True, null=True)

