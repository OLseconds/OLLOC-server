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

