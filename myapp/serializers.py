from myapp.models import User, Post
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'mail')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('first_name', 'last_name')
