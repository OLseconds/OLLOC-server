from django.db import models
import re


# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name="회원 아이디", max_length=30)
    password = models.CharField(verbose_name="회원 패스워드", max_length=30)
    name = models.CharField(verbose_name="회원 이름", max_length=15)
    mail = models.CharField(verbose_name="회원 이메일", max_length=30)


class Post(models.Model):
    first_name = models.CharField(verbose_name="이름", max_length=30)
    last_name = models.CharField(verbose_name="성", max_length=30)

