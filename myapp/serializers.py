from myapp.models import Posts, PostInfo
from rest_framework import serializers
from django.contrib.auth.models import User as authUser
from rest_framework.response import Response
from rest_framework.views import APIView


class UserSerializer(serializers.Serializer):
    class Meta:
        model = authUser
        fields = ('username', 'password', 'name', 'mail')


class PostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ('id', 'owner', 'last_modified', 'description')


class PostInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostInfo
        fields = ('post_id', 'lx', 'ly', 'map_info', 'img')


class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostInfo
        fields = ('post_id', 'owner', 'description', 'date', 'last_modified')